from string import Template

from llmmaster import LLMMaster
from llmmaster.utils import extract_llm_response

from .config import CLASS_DIAGRAM_GENERATION_PROMPT
from .config import DEFAULT_FREEDOM
from .config import DEFAULT_IDEAS
from .config import DEFAULT_LANGUAGE
from .config import EVALUATION_PROMPT
from .config import IDEA_GENERATION_PROMPT
from .config import IDEA_REDUCTION_PROMPT
from .config import KEY_CLASS_DIAGRAM
from .config import KEY_ELAPSED_TIME
from .config import KEY_EVALUATION
from .config import KEY_FREEDOM
from .config import KEY_IDEA_LIST
from .config import KEY_IDEA_REDUCTION
from .config import KEY_IDEAS
from .config import KEY_INPUT
from .config import KEY_LANGUAGE
from .config import KEY_MINDMAP
from .config import KEY_OUTPUT
from .config import KEY_THEME
from .config import LLM_IDEA_EVALUATION
from .config import LLM_IDEA_GENERATION
from .config import LLM_IDEA_ORGANIZATION
from .config import LLM_IDEA_REDUCTION
from .config import MINDMAP_GENERATION_PROMPT
from .config import PROGRESS_DONE
from .config import PROGRESS_FAILED
from .config import PROGRESS_IDEA_EVALUATION
from .config import PROGRESS_IDEA_GENERATION
from .config import PROGRESS_NOT_STARTED
from .config import PROGRESS_ORGANIZING
from .config import PROGRESS_REDUCING
from .config import PROGRESS_VERIFYING
from .config import WAIT_FOR_STARTING
from .utils import print_record
from .utils import remove_highlight
# from .utils import sanitize_mermaid
from .utils import strip_mermaid


class Monju:
    """
    Main class for Monju, multi-AI brainstorming framework.
    """
    def __init__(
        self,
        api_keys: str = '',
        verbose: bool = False,
        reduction: bool = False,
        **kwargs
    ) -> None:
        """
        Initialize the Monju class with the following parameters:
          System parameters:
            api_keys (str): API keys for LLMs in LLMMaster manner
            verbose (bool): print progress for debugging
            reduction (bool): remove duplicate ideas
          Brainstorming parameters as kwargs:
            theme (str) (required): theme or topic of brainstorming
            ideas (int): number of ideas to generate
            freedom (float): freedom value for LLM
            language (str): language for output
        """
        if not kwargs:
            raise ValueError("No parameters are given.")
        elif (not kwargs.get(KEY_THEME, None) or
              not isinstance(kwargs.get(KEY_THEME), str)):
            raise ValueError(f"{KEY_THEME} is not given or not str.")

        if kwargs.get(KEY_IDEAS, None) is None:
            kwargs[KEY_IDEAS] = DEFAULT_IDEAS
        if kwargs.get(KEY_FREEDOM, None) is None:
            kwargs[KEY_FREEDOM] = DEFAULT_FREEDOM
        if kwargs.get(KEY_LANGUAGE, None) is None:
            kwargs[KEY_LANGUAGE] = DEFAULT_LANGUAGE

        self.api_keys = api_keys
        self.verbose = verbose
        self.reduction = reduction
        self.status = PROGRESS_NOT_STARTED
        self.record = {
            KEY_INPUT: kwargs,
            KEY_OUTPUT: {
                KEY_ELAPSED_TIME: []
            }
        }

    def brainstorm(self) -> None:
        """
        Batch process of brainstorming
        """
        try:
            self.generate_ideas()
            self.reduce_ideas()
            self.organize_ideas()
            self.evaluate_ideas()
            self.verify()
        except Exception as e:
            msg = f"Error in batch process of brainstorming: {e}"
            raise Exception(msg) from e

    def generate_ideas(self, **kwargs) -> None:
        """
        Brainstorming Step 1: generate ideas
          kwargs: custom LLM setting in LLMMaster manner
        """
        self.status = PROGRESS_IDEA_GENERATION

        if self.verbose:
            print("Monju Step 1: Generating ideas...")

        try:
            master = LLMMaster(wait_for_starting=WAIT_FOR_STARTING)
            master.set_api_keys(self.api_keys)
            master.summon(self._llm_ideation(**kwargs))
            master.run()

            for key, value in master.results.items():
                master.results[key] = remove_highlight(
                    extract_llm_response(value)
                )
            self.record[KEY_OUTPUT][KEY_IDEAS] = master.results
            self.record[KEY_OUTPUT][KEY_IDEA_LIST] = '\n'.join(
                self.record[KEY_OUTPUT][KEY_IDEAS].values()
            )
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time
            )

        except Exception as e:
            self.status = PROGRESS_FAILED
            msg = f"Error in idea generation: {e}"
            raise Exception(msg) from e

    def reduce_ideas(self, **kwargs) -> None:
        """
        Preprocessing for Step 2: remove duplicate ideas
        """
        if not self.reduction:
            self.record[KEY_INPUT][KEY_IDEA_REDUCTION] = {}
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(0)
            return

        self.status = PROGRESS_REDUCING

        if self.verbose:
            print("Preprocessing: Removing duplicate ideas...")

        try:
            master = LLMMaster()
            master.set_api_keys(self.api_keys)
            master.summon(self._llm_reduction(**kwargs))
            master.run()

            self.record[KEY_OUTPUT][KEY_IDEA_LIST] = extract_llm_response(
                master.results[KEY_IDEA_REDUCTION]
            )
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time
            )

        except Exception as e:
            self.status = PROGRESS_FAILED
            msg = f"Error in idea reduction: {e}"
            raise Exception(msg) from e

    def organize_ideas(self, **kwargs) -> None:
        """
        Brainstorming Step 2: organize ideas into mindmap and class diagram
          kwargs: custom LLM setting in LLMMaster manner
        """
        self.status = PROGRESS_ORGANIZING

        if self.verbose:
            print("Monju Step 2: Organizing ideas...")

        try:
            master = LLMMaster()
            master.set_api_keys(self.api_keys)
            master.summon(self._llm_mindmap(**kwargs))
            master.summon(self._llm_class_diagram(**kwargs))
            master.run()

            buff = strip_mermaid(
                extract_llm_response(master.results[KEY_MINDMAP])
            )
            self.record[KEY_OUTPUT][KEY_MINDMAP] = buff

            buff = strip_mermaid(
                extract_llm_response(master.results[KEY_CLASS_DIAGRAM])
            )
            self.record[KEY_OUTPUT][KEY_CLASS_DIAGRAM] = buff

            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time
            )

        except Exception as e:
            self.status = PROGRESS_FAILED
            msg = f"Error in idea organization: {e}"
            raise Exception(msg) from e

    def evaluate_ideas(self, **kwargs) -> None:
        """
        Brainstorming Step 3: evaluate ideas
          kwargs: custom LLM setting in LLMMaster manner
        """
        self.status = PROGRESS_IDEA_EVALUATION

        if self.verbose:
            print("Monju Step 3: Evaluating ideas...")

        try:
            master = LLMMaster(wait_for_starting=WAIT_FOR_STARTING)
            master.set_api_keys(self.api_keys)
            master.summon(self._llm_evaluation(**kwargs))
            master.run()

            for key, value in master.results.items():
                master.results[key] = remove_highlight(
                    extract_llm_response(value)
                )
            self.record[KEY_OUTPUT][KEY_EVALUATION] = master.results
            self.record[KEY_OUTPUT][KEY_ELAPSED_TIME].append(
                master.elapsed_time
            )

        except Exception as e:
            self.status = PROGRESS_FAILED
            msg = f"Error in idea evaluation: {e}"
            raise Exception(msg) from e

    def verify(self) -> None:
        """
        Brainstorming step 4: Verify if all the steps are completed
          Note: not necessary to check elapsed time
        """
        self.status = PROGRESS_VERIFYING
        msg = ''

        if self.verbose:
            print("Monju Step 4: Verifying results...")
            print_record(self.record)

        if not self.record[KEY_OUTPUT][KEY_IDEAS]:
            msg += "Ideas are not generated. "
        if not self.record[KEY_OUTPUT][KEY_MINDMAP]:
            msg += "Mindmap is not generated. "
        if not self.record[KEY_OUTPUT][KEY_CLASS_DIAGRAM]:
            msg += "Class diagram is not generated. "
        if not self.record[KEY_OUTPUT][KEY_EVALUATION]:
            msg += "Evaluation is not done. "

        if msg:
            self.status = PROGRESS_FAILED
            raise Exception("Error in verification: "+msg)

        self.status = PROGRESS_DONE

    def _llm_ideation(self, **kwargs) -> dict:
        """
        LLM configuration for idea generation.
        """
        llm_config = kwargs if kwargs else LLM_IDEA_GENERATION

        self.record[KEY_INPUT][PROGRESS_IDEA_GENERATION] = llm_config

        prompt = Template(IDEA_GENERATION_PROMPT).safe_substitute(
            theme=self.record[KEY_INPUT][KEY_THEME],
            ideas=str(self.record[KEY_INPUT][KEY_IDEAS]),
            language=self.record[KEY_INPUT][KEY_LANGUAGE]
        )

        if self.verbose:
            print(f"Prompt:\n{prompt}")

        for _, parameters in llm_config.items():
            parameters["prompt"] = prompt
            parameters["temperature"] = self.record[KEY_INPUT][KEY_FREEDOM]

        return llm_config

    def _llm_reduction(self, **kwargs) -> dict:
        """
        LLM configuration for idea reduction.
        """
        llm_config = kwargs if kwargs else LLM_IDEA_REDUCTION

        self.record[KEY_INPUT][KEY_IDEA_REDUCTION] = \
            llm_config[KEY_IDEA_REDUCTION]

        prompt = Template(IDEA_REDUCTION_PROMPT).safe_substitute(
            idea_list=self.record[KEY_OUTPUT][KEY_IDEA_LIST],
            language=self.record[KEY_INPUT][KEY_LANGUAGE]
        )

        if self.verbose:
            print(f"Prompt:\n{prompt}")

        for _, parameters in llm_config.items():
            parameters["prompt"] = prompt

        return llm_config

    def _llm_mindmap(self, **kwargs) -> dict:
        """
        LLM configuration for mindmap generation.
        """
        llm_config = {
            KEY_MINDMAP: kwargs[KEY_MINDMAP]
            if KEY_MINDMAP in kwargs
            else LLM_IDEA_ORGANIZATION[KEY_MINDMAP]
        }

        self.record[KEY_INPUT][KEY_MINDMAP] = llm_config[KEY_MINDMAP]

        prompt = Template(MINDMAP_GENERATION_PROMPT).safe_substitute(
            theme=self.record[KEY_INPUT][KEY_THEME],
            idea_list=self.record[KEY_OUTPUT][KEY_IDEA_LIST],
            language=self.record[KEY_INPUT][KEY_LANGUAGE]
        )

        if self.verbose:
            print(f"Prompt:\n{prompt}")

        for _, parameters in llm_config.items():
            parameters["prompt"] = prompt

        return llm_config

    def _llm_class_diagram(self, **kwargs) -> dict:
        """
        LLM configuration for class diagram generation.
        """
        llm_config = {
            KEY_CLASS_DIAGRAM: kwargs[KEY_CLASS_DIAGRAM]
            if KEY_CLASS_DIAGRAM in kwargs
            else LLM_IDEA_ORGANIZATION[KEY_CLASS_DIAGRAM]
        }

        self.record[KEY_INPUT][KEY_CLASS_DIAGRAM] = \
            llm_config[KEY_CLASS_DIAGRAM]

        prompt = Template(CLASS_DIAGRAM_GENERATION_PROMPT).safe_substitute(
            theme=self.record[KEY_INPUT][KEY_THEME],
            idea_list=self.record[KEY_OUTPUT][KEY_IDEA_LIST],
            language=self.record[KEY_INPUT][KEY_LANGUAGE]
        )

        if self.verbose:
            print(f"Prompt:\n{prompt}")

        for _, parameters in llm_config.items():
            parameters["prompt"] = prompt

        return llm_config

    def _llm_evaluation(self, **kwargs) -> dict:
        """
        LLM configuration for idea evaluation.
        """
        llm_config = kwargs if kwargs else LLM_IDEA_EVALUATION

        self.record[KEY_INPUT][PROGRESS_IDEA_EVALUATION] = llm_config

        prompt = Template(EVALUATION_PROMPT).safe_substitute(
            theme=self.record[KEY_INPUT][KEY_THEME],
            mermaid_mindmap=self.record[KEY_OUTPUT][KEY_MINDMAP],
            language=self.record[KEY_INPUT][KEY_LANGUAGE]
        )

        if self.verbose:
            print(f"Prompt:\n{prompt}")

        for _, parameters in llm_config.items():
            parameters["prompt"] = prompt

        return llm_config
