from collections.abc import Collection, Sequence
from operator import attrgetter
from pathlib import Path

from attrs import frozen

from kumir_compose.preprocessor.exceptions import (
    IncludeFileNotFoundException,
    UnexpectedTokenException,
)
from kumir_compose.preprocessor.lexer import scan_file
from kumir_compose.preprocessor.tokens import Token, TokenType


@frozen
class Condition:
    name: str
    expected: bool


class Preprocessor:
    def __init__(
            self,
            filename: str,
            source: str,
            tokens: Sequence[Token],
            *,
            lookup_paths: Collection[str],
            encoding: str | None = None
    ) -> None:
        self._tokens = list(tokens)
        self._pos = 0
        self._filename = filename
        self._source = source
        self._macro_table: dict[str, Sequence[Token]] = {}
        self._macro_arg_table: dict[str, Sequence[str]] = {}
        self._lookup_paths = set(lookup_paths)
        self._lookup_paths.add("")
        self._encoding = encoding
        self._condition_stack = []
        self._included = set()

    @property
    def _at_end(self) -> bool:
        return self._pos >= len(self._tokens)

    def _next(self) -> Token | None:
        if self._at_end:
            return None
        self._pos += 1
        return self._tokens[self._pos - 1]

    @property
    def _peek(self) -> Token | None:
        if self._at_end:
            return None
        return self._tokens[self._pos]

    @property
    def _previous(self) -> Token:
        return self._tokens[self._pos - 1]

    def _match(
            self,
            expected_type: TokenType,
    ) -> Token | None:
        if self._at_end:
            return None
        if self._peek.type == expected_type:
            return self._next()
        return None

    def _match_lexeme(
            self,
            expected: str,
    ) -> Token | None:
        if self._at_end:
            return None
        if self._peek.lexeme == expected:
            return self._next()
        return None

    def _error(self, exc_type, offset: int = 0, *args, **kwargs):
        kwargs["source"] = self._source
        kwargs["filename"] = self._filename
        kwargs["token"] = self._tokens[
            min(len(self._tokens) - 1, max(self._pos + offset, 0))
        ]
        raise exc_type(*args, **kwargs)

    def _require(
            self,
            expected_type: TokenType,
            *,
            message: str | None = None,
    ) -> Token:
        token = self._match(expected_type)
        if token is None:
            self._error(
                UnexpectedTokenException,
                expected=expected_type,
                got=self._peek,
                message=message,
            )
        return token

    def _require_lexeme(
            self,
            expected_lexeme: str,
            *,
            message: str | None = None,
    ) -> Token:
        token = self._match_lexeme(expected_lexeme)
        if token is None:
            self._error(
                UnexpectedTokenException,
                expected=expected_lexeme,
                got=self._peek,
                message=message,
            )
        return token

    def _consume_spaces(self) -> None:
        while self._match(TokenType.SPACE): ...

    def process(self):
        """Run preprocessor."""
        processed = ""
        while not self._at_end:
            token = self._next()
            if token.type == TokenType.ENDIF:
                self._end_conditional()
                continue
            if not self._do_conditions_match():
                continue
            match token.type:
                case TokenType.DEFINE:
                    self._define_macro()
                case TokenType.UNDEF:
                    self._undef_macro()
                case TokenType.INCLUDE:
                    self._include()
                case TokenType.IFDEF:
                    self._start_conditional(expected=True)
                case TokenType.IFNDEF:
                    self._start_conditional(expected=False)
                case TokenType.ID:
                    new_token = self._process_id(token)
                    if new_token.lexeme != token.lexeme:
                        self._pos -= 1
                    else:
                        processed += new_token.lexeme
                case _:
                    processed += token.lexeme
        return processed

    def _define_macro(self) -> None:
        self._consume_spaces()
        macro_name = self._require(TokenType.ID)
        self._consume_spaces()
        if self._peek == TokenType.NEWLINE:
            self._match(TokenType.NEWLINE)
            self._macro_table[macro_name.value] = []
            return
        args = None
        if self._peek and self._peek.lexeme == "(":
            self._next()
            args = []
            while True:
                self._consume_spaces()
                args.append(self._require(TokenType.DEF_ARG).lexeme)
                self._consume_spaces()
                if not self._match_lexeme(","):
                    break
            self._require_lexeme(")")
        esc = False
        macro_values = []
        while self._peek:
            if self._peek.type == TokenType.NEWLINE:
                if esc:
                    esc = False
                else:
                    break
            if self._peek.lexeme == "\\":
                esc = True
                self._next()
            else:
                macro_values.append(self._next())
        self._macro_table[macro_name.value] = macro_values
        self._macro_arg_table[macro_name.value] = args

    def _undef_macro(self) -> None:
        self._consume_spaces()
        macro_name = self._require(TokenType.ID)
        if macro_name.value in self._macro_table:
            self._macro_table.pop(macro_name.value)
        if macro_name.value in self._macro_table:
            self._macro_table.pop(macro_name.value)

    def _include(self) -> None:
        self._consume_spaces()
        path_tok = self._match(TokenType.ID)
        if not path_tok:
            path_tok = self._require(TokenType.STRING)
        found_path = self._find_file(path_tok.value)
        if not found_path:
            self._error(
                IncludeFileNotFoundException,
                incl_file=path_tok.value,
                offset=-2
            )
        abs_path = str(found_path.absolute())
        if abs_path in self._included:
            return
        tokens = scan_file(abs_path, self._encoding)
        self._insert_tokens_here(list(tokens))
        self._included.add(abs_path)

    def _insert_tokens_here(self, tokens: list[Token]) -> None:
        self._tokens = (
            self._tokens[:self._pos] +
            list(tokens) +
            self._tokens[self._pos:]
        )

    def _find_file(self, filename) -> Path | None:
        for root in self._lookup_paths:
            if Path(root, filename).exists():
                return Path(root, filename)
            if Path(root, f"{filename}.kum").exists():
                return Path(root, f"{filename}.kum")
        return None

    def _start_conditional(self, *, expected: bool) -> None:
        self._consume_spaces()
        def_name = self._require(TokenType.ID)
        self._condition_stack.append(Condition(
            name=def_name.value,
            expected=expected
        ))

    def _end_conditional(self) -> None:
        self._condition_stack.pop()

    def _do_conditions_match(self) -> bool:
        for condition in self._condition_stack:
            is_present = condition.name in self._macro_table
            if is_present != condition.expected:
                return False
        return True

    def _process_id(self, token: Token) -> Token:
        if (
                token.lexeme in self._macro_table and
                not self._macro_arg_table.get(token.lexeme)
        ):
            first_token, *other_tokens = self._macro_table[token.lexeme]
            self._tokens[self._pos - 1] = first_token
            self._insert_tokens_here(other_tokens)
            return first_token
        if (
                token.lexeme in self._macro_table and
                self._macro_arg_table.get(token.lexeme)
        ):
            self._consume_spaces()
            self._require_lexeme("(")
            substitute = {}
            for arg in self._macro_arg_table[token.lexeme]:
                self._consume_spaces()
                tokens = []
                while self._peek and self._peek.lexeme not in ",)":
                    tokens.append(self._next())
                substitute[arg] = tokens
                if self._peek.lexeme == ")":
                    break
                self._require_lexeme(",")
            self._require_lexeme(")")
            tokens = self._macro_table[token.lexeme]
            substituted_tokens = []
            for token in tokens:
                if (
                        token.type == TokenType.DEF_ARG and
                        token.lexeme in substitute
                ):
                    substituted_tokens.extend(substitute[token.lexeme])
                elif token.type in (TokenType.COMMENT, TokenType.STRING):
                    substituted_tokens.append(Token(
                        type=token.type,
                        char=token.char,
                        line=token.line,
                        value=_replace_vars_in_str(token.value, substitute),
                        lexeme=_replace_vars_in_str(token.lexeme, substitute),
                    ))
                else:
                    substituted_tokens.append(token)
            first_token, *other_tokens = substituted_tokens
            self._tokens[self._pos - 1] = first_token
            self._insert_tokens_here(other_tokens)
            return first_token
        return token


def _replace_vars_in_str(
        text: str, variables: dict[str, Sequence[Token]]
) -> str:
    for var_name, var_value in variables.items():
        text = text.replace(
            f"${var_name}$",
            "".join(map(attrgetter("lexeme"), var_value))
        )
    return text
