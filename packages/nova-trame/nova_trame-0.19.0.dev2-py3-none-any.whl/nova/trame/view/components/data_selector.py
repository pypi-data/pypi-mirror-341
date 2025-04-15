"""View Implementation for DataSelector."""

from typing import Any, Optional, cast

from trame.app import get_server
from trame.widgets import html
from trame.widgets import vuetify3 as vuetify

from nova.mvvm.trame_binding import TrameBinding
from nova.trame.model.data_selector import DataSelectorModel
from nova.trame.view.layouts import GridLayout
from nova.trame.view_model.data_selector import DataSelectorViewModel

from .input_field import InputField

vuetify.enable_lab()


class DataSelector(vuetify.VDataTable):
    """Allows the user to select datafiles from an IPTS experiment."""

    def __init__(
        self,
        v_model: str,
        facility: str = "",
        instrument: str = "",
        prefix: str = "",
        select_strategy: str = "all",
        **kwargs: Any,
    ) -> None:
        """Constructor for DataSelector.

        Parameters
        ----------
        v_model : str
            The name of the state variable to bind to this widget. The state variable will contain a list of the files
            selected by the user.
        facility : str, optional
            The facility to restrict data selection to. Options: HFIR, SNS
        instrument : str, optional
            The instrument to restrict data selection to. Please use the instrument acronym (e.g. CG-2).
        prefix : str, optional
            A subdirectory within the user's chosen experiment to show files. If not specified, the user will be shown a
            folder browser and will be able to see all files in the experiment that they have access to.
        select_strategy : str, optional
            The selection strategy to pass to the `VDataTable component <https://trame.readthedocs.io/en/latest/trame.widgets.vuetify3.html#trame.widgets.vuetify3.VDataTable>`__.
            If unset, the `all` strategy will be used.
        **kwargs
            All other arguments will be passed to the underlying
            `VDataTable component <https://trame.readthedocs.io/en/latest/trame.widgets.vuetify3.html#trame.widgets.vuetify3.VDataTable>`_.

        Returns
        -------
        None
        """
        if "items" in kwargs:
            raise AttributeError("The items parameter is not allowed on DataSelector widget.")

        if "label" in kwargs:
            self._label = kwargs["label"]
        else:
            self._label = None

        self._v_model = v_model
        self._prefix = prefix
        self._select_strategy = select_strategy

        self._state_name = f"nova__dataselector_{self._next_id}_state"
        self._facilities_name = f"nova__dataselector_{self._next_id}_facilities"
        self._instruments_name = f"nova__dataselector_{self._next_id}_instruments"
        self._experiments_name = f"nova__dataselector_{self._next_id}_experiments"
        self._directories_name = f"nova__dataselector_{self._next_id}_directories"
        self._datafiles_name = f"nova__dataselector_{self._next_id}_datafiles"

        self.create_model(facility, instrument)
        self.create_viewmodel()

        self.create_ui(facility, instrument, **kwargs)

    def create_ui(self, facility: str, instrument: str, **kwargs: Any) -> None:
        with GridLayout(columns=3):
            columns = 3
            if facility == "":
                columns -= 1
                InputField(v_model=f"{self._state_name}.facility", items=(self._facilities_name,), type="autocomplete")
            if instrument == "":
                columns -= 1
                InputField(
                    v_model=f"{self._state_name}.instrument", items=(self._instruments_name,), type="autocomplete"
                )
            InputField(
                v_model=f"{self._state_name}.experiment",
                column_span=columns,
                items=(self._experiments_name,),
                type="autocomplete",
            )

        with GridLayout(columns=3, valign="start"):
            if not self._prefix:
                with html.Div():
                    vuetify.VListSubheader("Available Directories", classes="justify-center px-0")
                    vuetify.VTreeview(
                        v_if=(f"{self._directories_name}.length > 0",),
                        activatable=True,
                        active_strategy="single-independent",
                        item_value="path",
                        items=(self._directories_name,),
                        update_activated=(self._vm.set_directory, "$event"),
                    )
                    vuetify.VListItem("No directories found", v_else=True)

            super().__init__(
                v_model=self._v_model,
                column_span=3 if self._prefix else 2,
                headers=("[{ align: 'center', key: 'title', title: 'Available Datafiles' }]",),
                item_title="title",
                item_value="path",
                select_strategy=self._select_strategy,
                show_select=True,
                **kwargs,
            )
            self.items = (self._datafiles_name,)
            if "update_modelValue" not in kwargs:
                self.update_modelValue = f"flushState('{self._v_model.split('.')[0]}')"

        with cast(
            vuetify.VSelect,
            InputField(
                v_if=f"{self._v_model}.length > 0",
                v_model=self._v_model,
                classes="nova-readonly",
                clearable=True,
                label=self._label,
                readonly=True,
                type="select",
            ),
        ):
            with vuetify.Template(raw_attrs=['v-slot:selection="{ item, index }"']):
                vuetify.VChip("{{ item.title }}", v_if="index < 2")
                html.Span(f"(+{{{{ {self._v_model}.length - 2 }}}} others)", v_if="index === 2", classes="text-caption")

    def create_model(self, facility: str, instrument: str) -> None:
        self._model = DataSelectorModel(facility, instrument, self._prefix)

    def create_viewmodel(self) -> None:
        server = get_server(None, client_type="vue3")
        binding = TrameBinding(server.state)

        self._vm = DataSelectorViewModel(self._model, binding)
        self._vm.state_bind.connect(self._state_name)
        self._vm.facilities_bind.connect(self._facilities_name)
        self._vm.instruments_bind.connect(self._instruments_name)
        self._vm.experiments_bind.connect(self._experiments_name)
        self._vm.directories_bind.connect(self._directories_name)
        self._vm.datafiles_bind.connect(self._datafiles_name)

        self._vm.update_view()

    def set_state(
        self, facility: Optional[str] = None, instrument: Optional[str] = None, experiment: Optional[str] = None
    ) -> None:
        """Programmatically set the facility, instrument, and/or experiment to restrict data selection to.

        If a parameter is None, then it will not be updated.

        Parameters
        ----------
        facility : str, optional
            The facility to restrict data selection to. Options: HFIR, SNS
        instrument : str, optional
            The instrument to restrict data selection to. Must be at the selected facility.
        experiment : str, optional
            The experiment to restrict data selection to. Must begin with "IPTS-". It is your responsibility to validate
            that the provided experiment exists within the instrument directory. If it doesn't then no datafiles will be
            shown to the user.

        Returns
        -------
        None
        """
        self._vm.set_state(facility, instrument, experiment)
