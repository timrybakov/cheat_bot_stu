from typing import Optional, Dict, Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StateType


class FSMPresenter:
    def __init__(self, state: FSMContext):
        self.__state = state

    async def clear_state(self) -> None:
        await self.__state.clear()

    async def get_data(self) -> Dict[str, Any]:
        return await self.__state.storage.get_data(key=self.__state.key)

    async def set_data(self, data: Dict[str, Any]) -> None:
        await self.__state.storage.set_data(key=self.__state.key, data=data)

    async def update_data(
            self,
            data: Optional[Dict[str, Any]] = None,
            **kwargs: Any
    ) -> Dict[str, Any]:
        if data:
            kwargs.update(data)
        return await self.__state.storage.update_data(key=self.__state.key, data=kwargs)

    async def set_state(self, new_state: StateType = None) -> None:
        await self.__state.storage.set_state(key=self.__state.key, state=new_state)

    async def clear(self) -> None:
        await self.set_state(new_state=None)
        await self.set_data({})
