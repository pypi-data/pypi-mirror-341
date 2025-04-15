from tketool.lmc.lmc_linked_flow import *
from tketool.ml.modelbase import *


class lmc_linked_flow_fix(lmc_linked_flow_model, Model_Base):
    @property
    def model_name(self):
        return self._model_name

    def __init__(self, prompt_file: prompt_define_file, llm, fix_llm=None,
                 model_name=None, retry_time=3, merge_update=True, txt_log_folder_path=None, save_path=None):
        self.fix_llm = fix_llm if fix_llm is not None else llm
        self._model_name = model_name
        self._merge_update = merge_update
        self.log_folder_path = txt_log_folder_path
        Model_Base.__init__(self, save_path=save_path)
        for pk, pro in prompt_file.prompts.items():
            p_key = pk + "_step"
            self.save_variables[p_key] = []
            pro.prompt_content += "\n\n  按照下面的步骤完成: \n {" + p_key + "}"

        lmc_linked_flow_model.__init__(self, llm, prompt_file, retry_time=retry_time,
                                       folder_log_path=txt_log_folder_path)

        self.step_init_invoke = None
        self.fix_invoke = None
        self.merge_invoke = None

    def _init_step(self, p_key, ori_prompt: str, ):
        if self.step_init_invoke is None:
            step_init_prompt = get_prompt("step_init", lang="chinese")
            self.step_init_invoke = lmc_linked_flow_model(self.fix_llm, step_init_prompt,
                                                          folder_log_path=self.log_folder_path,
                                                          retry_time=2)
        step_init_result = self.step_init_invoke(prompt=ori_prompt)
        self.save_variables[p_key] = step_init_result.result.step

    def __call__(self, **kwargs):
        step_dict = {}
        for pk, pro in self.define_file.prompts.items():
            p_key = pk + "_step"
            if len(self.save_variables[p_key]) == 0:
                self._init_step(p_key, pro.prompt_content)
            step_dict[p_key] = "\n".join(self.save_variables[p_key])

        return lmc_linked_flow_model.__call__(self, **kwargs, **step_dict)

    def fix(self, label_result: str, original_result=None, fix_prompt_name: str = "default",
            result_func_convert=None, **kwargs):
        if self.fix_invoke is None:
            step_fix_prompt = get_prompt("step_fix", lang="chinese")
            self.fix_invoke = lmc_linked_flow_model(self.fix_llm, step_fix_prompt, retry_time=2,
                                                    folder_log_path=self.log_folder_path, )
            if self._merge_update:
                merge_fix_prompt = get_prompt("step_merge", lang="chinese")
                self.merge_invoke = lmc_linked_flow_model(self.fix_llm, merge_fix_prompt, retry_time=2,
                                                          folder_log_path=self.log_folder_path, )

        # call model
        if original_result is None:
            original_result = self(**kwargs)

        for pname, presult, plog, pv_list in zip(original_result.results_invoke_prompt,
                                                 original_result.results,
                                                 original_result.sub_process_logs,
                                                 original_result.template_value_list):
            if pname == fix_prompt_name:
                l_model = self.linked_model[pname]
                template = l_model.original_prompt_template
                prompt_str = template.format(last=pv_list, **original_result.template_value)
                if result_func_convert is not None:
                    ori_result = result_func_convert(presult)
                else:
                    ori_result = presult.json()
                p_key = pname + "_step"
                step_fix_result = self.fix_invoke(prompt=prompt_str,
                                                  # step="\n".join(self.save_variables[p_key]),
                                                  llm_result=ori_result,
                                                  right_result=label_result
                                                  )
                if self._merge_update:
                    merge_Result = self.merge_invoke(step1="\n".join(self.save_variables[p_key]),
                                                     step2="\n".join(step_fix_result.result.steps))
                    if merge_Result.result is not None:
                        self.save_variables[p_key] = merge_Result.result.steps
                    else:
                        self.save_variables[p_key] = step_fix_result.result.steps
                else:
                    self.save_variables[p_key] = step_fix_result.result.steps
