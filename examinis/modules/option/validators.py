from typing import List

from pydantic import BaseModel, field_validator

from examinis.modules.option.schemas import OptionInSchema

MIN_OPTIONS = 2
MAX_OPTIONS = 5


class OptionsValidationMixin:
    @field_validator('options')
    @classmethod
    def validate_options(
        cls, options: List[OptionInSchema]
    ) -> List[OptionInSchema]:
        if not (MIN_OPTIONS <= len(options) <= MAX_OPTIONS):
            raise ValueError(
                f'A question must have between {MIN_OPTIONS} and {MAX_OPTIONS} options.'
            )
        return options

    @field_validator('options')
    @classmethod
    def check_unique_options(
        cls, options: List[OptionInSchema]
    ) -> List[OptionInSchema]:
        descriptions = set()
        letters = set()

        for option in options:
            if option.description in descriptions:
                raise ValueError(
                    f'Duplicate option description: {option.description}'
                )
            if option.letter in letters:
                raise ValueError(f'Duplicate option letter: {option.letter}')

            descriptions.add(option.description)
            letters.add(option.letter)

        return options
