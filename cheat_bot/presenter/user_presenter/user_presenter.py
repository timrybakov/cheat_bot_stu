from typing import Any, Dict

from aiogram import types
from aiogram.fsm.context import FSMContext


from cheat_bot.clients.utils import AccessHelper
from cheat_bot.config.config import settings
from cheat_bot.di.di import depends
from cheat_bot.model.fsm.storage import UserCallbackData
from cheat_bot.model.validators.validators import InsertValidator
from cheat_bot.presenter.fsm_presenter.fsm_presenter import FSMPresenter


class UserPresenter:
    def __init__(self, state: FSMContext = None):
        self.__state = state

    @property
    def get_fsm_storage(self) -> FSMPresenter:
        return FSMPresenter(self.__state)

    def on_start_check_permission(self, id_: int):
        if settings.ADMIN_GROUP_ID == id_:
            return

    def send_to_s3_storage(self, image_id: str, bucket_name: str, file_path: str) -> None:
        image = AccessHelper.get_images_binary(image_id)
        image_bin = AccessHelper.convert_bin_to_jpg(image)
        depends.repository_container.s3_interface.add(image_bin, bucket_name, file_path)

    async def post_image(self, **kwargs: dict) -> None:
        try:
            validated_data = InsertValidator(**kwargs)
            await depends.repository_container.user_interface.create(
                **validated_data.model_dump()
            )
        except ValueError:
            raise ValueError

    async def select_and_delete_from_database(self):
        result = await depends.repository_container.user_interface.get_first()
        await depends.repository_container.user_interface.delete(id_=result.id)
        return result

    async def set_method(
            self,
            query: types.CallbackQuery,
            fsm_storage: dict
    ) -> None:
        if fsm_storage.get('method') == 'post':
            await self.get_fsm_storage.set_data({})
            await self.get_fsm_storage.update_data(
                bucket=query.data.split(':')[1],
                user_telegram_id=query.from_user.id,
                username=fsm_storage.get('username')
            )
            await self.get_fsm_storage.set_state(UserCallbackData.post)
        else:
            await self.get_fsm_storage.set_data({})
            await self.get_fsm_storage.update_data(
                bucket=query.data.split(':')[1],
                user_telegram_id=query.from_user.id,
                username=fsm_storage.get('username')
            )
            await self.get_fsm_storage.set_state(UserCallbackData.get)

    async def get_all_images(self, message: types.Message) -> tuple[list, Dict[str, Any]]:
        fsm_storage = await self.get_fsm_storage.get_data()
        bucket_name = fsm_storage.get('bucket')
        list_of_images = depends.repository_container.s3_interface.get(
            bucket_name=bucket_name, route=message.text.lower()
        )
        return list_of_images, fsm_storage
