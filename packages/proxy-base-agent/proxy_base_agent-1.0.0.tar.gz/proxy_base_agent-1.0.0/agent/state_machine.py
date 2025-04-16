from pse.types.base.any import AnyStateMachine
from pse.types.base.loop import LoopStateMachine
from pse_core.state_machine import StateMachine

from agent.state import (
    AgentState,
    InnerMonologue,
    Python,
    Scratchpad,
    Thinking,
    ToolCallState,
)
from agent.tools import Tool


class AgentStateMachine(StateMachine):
    """
        State machine orchestrating the agent's planning and action phases.

                        ┌───────────────────┐
                        │                   │
                        ▼                   │
            ┌──────────────────────────────────────────────────┐
            │                   PLAN                           │ ◀─ loops (min=x, max=y)
            │ ┌─────────┐  ┌──────────┐  ┌───────────────┐     │
            │ │THINKING │  │SCRATCHPAD│  │INNER MONOLOGUE│     │
            │ └─────────┘  └──────────┘  └───────────────┘     │
            └────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
                ┌───────────────────────────────┐
                │           TAKE ACTION         │
                │ ┌─────────┐ ┌────────┐        │
                │ │  TOOLS  │ │ PYTHON │        │
                │ └────┬────┘ └───┬────┘        │
                └──────┼──────────┼─────────────┘
                       │          │
                       └──────────┼──────────────
                                  ▼
                            ┌─────────┐
                            │  DONE   │
                            └─────────┘

    Explanation:
    - The agent begins in PLAN, iteratively cycling (min=x, max=y loops) through the unordered states: THINKING, SCRATCHPAD, and INNER MONOLOGUE.
    - After planning, it transitions into TAKE ACTION, selecting among TOOLS or PYTHON.
    - Upon completing the action phase, the agent transitions into DONE.
    """

    def __init__(
        self,
        tools: list[Tool] | None = None,
        use_python: bool = False,
        force_planning: bool = True,
        max_planning_loops: int = 3,
        delimiters_kwargs: dict[str, tuple[str, str] | None] | None = None,
        character_max: int | None = None,
    ) -> None:
        """
        Initialize the agent state machine with specific capabilities.

        Args:
            tools: List of Tool objects available to the agent
            use_python: Whether to enable Python code execution
            force_planning: If True, require at least one planning loop
            max_planning_loops: Maximum number of planning iterations
            delimiters_kwargs: Custom delimiters for state boundary markers
            character_max: Maximum character limit for state outputs
        """
        self.states: dict[str, AgentState] = {}
        delimiters = delimiters_kwargs or {}
        planning_states = self.create_planning_states(character_max, **delimiters)
        action_states = self.create_action_states(
            tools,
            use_python,
            **delimiters,
        )

        super().__init__(
            {
                "plan": [
                    (
                        LoopStateMachine(
                            AnyStateMachine(planning_states),
                            min_loop_count=int(force_planning),
                            max_loop_count=max_planning_loops,
                            whitespace_seperator=True,
                        ),
                        "take_action",
                    )
                ],
                "take_action": [(action, "done") for action in action_states],
            },
            start_state="plan",
            end_states=["done"],
        )

    def create_planning_states(
        self,
        character_max: int | None = None,
        **delimiters: tuple[str, str] | None,
    ) -> list[StateMachine]:
        """
        Create and configure all planning phase states.

        Planning states allow the agent to reason through problems before taking action.
        Each state serves a specific cognitive function in the planning process.

        Args:
            character_max: Maximum character limit for state outputs
            **delimiters: Custom delimiters for different states

        Returns:
            List of StateMachine objects for planning states
        """
        # Use a default character limit of 1000 if not specified
        char_limit = character_max or 1000

        # Thinking: Initial problem analysis and approach planning
        thinking_state = Thinking(delimiters.get("thinking"), character_max=char_limit)
        self.states[thinking_state.identifier] = thinking_state

        # Scratchpad: Workspace for notes, calculations, and data organization
        scratchpad_state = Scratchpad(
            delimiters.get("scratchpad"), character_max=char_limit
        )
        self.states[scratchpad_state.identifier] = scratchpad_state

        # Inner Monologue: Self-reflective consideration of approach and reasoning
        inner_monologue_state = InnerMonologue(
            delimiters.get("inner_monologue"), character_max=char_limit
        )
        self.states[inner_monologue_state.identifier] = inner_monologue_state

        return [
            thinking_state.state_machine,
            scratchpad_state.state_machine,
            inner_monologue_state.state_machine,
        ]

    def create_action_states(
        self,
        tools: list[Tool] | None = None,
        use_python: bool = False,
        **delimiters: tuple[str, str] | None,
    ) -> list[StateMachine]:
        """
        Create and configure all action phase states.

        Action states enable the agent to interact with its environment through
        various mechanisms, such as tools or code execution.

        Args:
            tools: List of Tool objects to make available for tool calls
            use_python: Whether to enable Python code execution state
            **delimiters: Custom delimiters for different states

        Returns:
            List of StateMachine objects for action states

        Note:
            At least one action state must be enabled for the agent to function.
            If no action states are enabled, the agent would have no way to
            interact with its environment.
        """
        action_states = []

        # Tool Call State: For invoking specialized tools
        if tools:
            tool_state = ToolCallState(
                tools,
                delimiters.get("tool_call"),
                delimiters.get("tool_list"),
            )
            self.states[tool_state.identifier] = tool_state
            action_states.append(tool_state.state_machine)

        # Python State: For executing Python code
        if use_python:
            python_state = Python()
            self.states[python_state.identifier] = python_state
            action_states.append(python_state.state_machine)

        return action_states

    @property
    def prompt(self) -> str:
        """
        Creates a comprehensive explanation of how the agent's state machine works.
        """

        states_str = "\n".join(str(state) for state in self.states.values())

        return f"""
An agentic system operates through a sequence of states to interact with its environment.

State Transitions:
- Move between states using delimiters to indicate the start and end of a state.
- Each transition should be purposeful and advance toward an underlying goal.
- Do not be overly verbose or repeat yourself.

Available States:

{states_str}

You interact with the user exclusively through the "send message" tool.
No direct output or dialogue should occur outside this tool.
Time spent outside of sending message is added latency to your response.

Nested states are NOT allowed.
State transitions must be explicit, singular, and clearly defined.
States occur sequentially, one after the other, not simultaneously.

Do not pendanticly address your own state transitions or current state.
Do not repeat yourself across states or hallucinate unexisting states.
        """
