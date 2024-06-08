from typing import Any, Dict

from aiogram import types
from aiogram.fsm.context import FSMContext

from cheat_bot.model import sсhemes, s3_storage, postgres
from ..conversion import Conversion
from ..error_handlers import custom_errors
from ..fsm_presenter import fsm_presenter


class UserPresenter:
    def __init__(self, state: FSMContext = None) -> None:
        self._state = state
        self._s3_conn = s3_storage.S3Storage()
        self._postgres_conn = postgres.PostgresCommunication()

    @property
    def get_fsm_storage(self) -> fsm_presenter.FSMPresenter:
        return fsm_presenter.FSMPresenter(self._state)

    def send_to_s3_storage(self, image_id: str, academy_year: str, file_path: str) -> None:
        image_bin = Conversion.convert_bin_to_jpg(image_id)
        self._s3_conn.post(image_bin, academy_year, file_path)

    async def post_image(self, kwargs: dict) -> None:
        try:
            validated_data = sсhemes.UserScheme(**kwargs)
            await self._postgres_conn.create(validated_data)
        except custom_errors.NotUniqueException:
            raise custom_errors.NotUniqueException()
        except ValueError:
            raise custom_errors.AfterValidationException()

    async def get_first_obj(self) -> sсhemes.UserScheme:
        try:
            result = await self._postgres_conn.select()
            await self._postgres_conn.delete(obj=result)
            return result
        except custom_errors.NoMaterialException:
            raise custom_errors.NoMaterialException()

    async def set_user_interaction_method(
            self,
            query: types.CallbackQuery,
            fsm_storage: dict
    ):
        await self.get_fsm_storage.set({})
        await self.get_fsm_storage.update(
            academy_year=query.data.split(':')[1],
            telegram_id=query.from_user.id,
            username=fsm_storage.get('username')
        )

    async def get_all_images(self, message: types.Message) -> tuple[list, Dict[str, Any]]:
        fsm_storage = await self.get_fsm_storage.get()
        academy_year = fsm_storage.get('academy_year')
        list_of_images = self._s3_conn.get(
            academy_year=academy_year, route=message.text.lower()
        )
        return list_of_images, fsm_storage
