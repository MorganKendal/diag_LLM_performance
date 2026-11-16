import pandas as pd
from openpyxl import load_workbook
from processor import build_prompt, process_response
from api_calls import run_openai_call, run_gemini_call, run_claude_call



if __name__ == "__main__":
    # File and sheet names have been anonymized to preserve confidentiality.
    df = pd.read_excel("<Response_File_Name>", keep_default_na=False, sheet_name="Form Responses 1")
    new_cols = ["GPT_Çocuk_TanıVarYok", "GPT_Çocuk_1", "GPT_Çocuk_2", "GPT_Çocuk_3",
                "GPT_Ebeveyn_TanıVarYok", "GPT_Ebeveyn_1", "GPT_Ebeveyn_2", "GPT_Ebeveyn_3",
                "GPT_Çocuk + Ebeveyn_TanıVarYok", "GPT_Çocuk + Ebeveyn_1", "GPT_Çocuk + Ebeveyn_2", "GPT_Çocuk + Ebeveyn_3",
                "GPT_Çocuk + Ebeveyn + Hekim Muayenesi_TanıVarYok", "GPT_Çocuk + Ebeveyn + Hekim Muayenesi_1",
                "GPT_Çocuk + Ebeveyn + Hekim Muayenesi_2", "GPT_Çocuk + Ebeveyn + Hekim Muayenesi_3",

                "GEMINI_Çocuk_TanıVarYok", "GEMINI_Çocuk_1", "GEMINI_Çocuk_2", "GEMINI_Çocuk_3",
                "GEMINI_Ebeveyn_TanıVarYok", "GEMINI_Ebeveyn_1", "GEMINI_Ebeveyn_2", "GEMINI_Ebeveyn_3",
                "GEMINI_Çocuk + Ebeveyn_TanıVarYok", "GEMINI_Çocuk + Ebeveyn_1", "GEMINI_Çocuk + Ebeveyn_2", "GEMINI_Çocuk + Ebeveyn_3",
                "GEMINI_Çocuk + Ebeveyn + Hekim Muayenesi_TanıVarYok", "GEMINI_Çocuk + Ebeveyn + Hekim Muayenesi_1",
                "GEMINI_Çocuk + Ebeveyn + Hekim Muayenesi_2", "GEMINI_Çocuk + Ebeveyn + Hekim Muayenesi_3",

                "CLAUDE_Çocuk_TanıVarYok", "CLAUDE_Çocuk_1", "CLAUDE_Çocuk_2", "CLAUDE_Çocuk_3",
                "CLAUDE_Ebeveyn_TanıVarYok", "CLAUDE_Ebeveyn_1", "CLAUDE_Ebeveyn_2", "CLAUDE_Ebeveyn_3",
                "CLAUDE_Çocuk + Ebeveyn_TanıVarYok", "CLAUDE_Çocuk + Ebeveyn_1", "CLAUDE_Çocuk + Ebeveyn_2", "CLAUDE_Çocuk + Ebeveyn_3",
                "CLAUDE_Çocuk + Ebeveyn + Hekim Muayenesi_TanıVarYok", "CLAUDE_Çocuk + Ebeveyn + Hekim Muayenesi_1",
                "CLAUDE_Çocuk + Ebeveyn + Hekim Muayenesi_2", "CLAUDE_Çocuk + Ebeveyn + Hekim Muayenesi_3"]

    df = df.assign(**{col: "" for col in new_cols})

    # The base prompt was stored in the same Excel file, in a separate sheet.
    workbook = load_workbook("<Response_File_Name>")
    sheet = workbook["<Base_Prompt_Sheet>"]
    base_prompt = sheet["A1"].value

    try:
        for i in range(len(df)):
            prompts = build_prompt(base_prompt, df.iloc[i])
            responses = {}
            try:
                print(f"{df.iloc[i, 1]}... ", end="")
                for p in prompts:
                    print("GPT... ", end="")
                    gpt_response = run_openai_call(prompts[p])
                    diag, evals = process_response(gpt_response)
                    start = df.columns.get_loc(f"GPT_{p}_TanıVarYok")
                    df.iloc[i, start] = "Var" if diag else "Yok"
                    if diag:
                        df.iloc[i, start + 1:start + 4] = evals

                    print("Gemini... ", end="")
                    gemini_response = run_gemini_call(prompts[p])
                    diag, evals = process_response(gemini_response)
                    start = df.columns.get_loc(f"GEMINI_{p}_TanıVarYok")
                    df.iloc[i, start] = "Var" if diag else "Yok"
                    if diag:
                        df.iloc[i, start + 1:start + 4] = evals

                    print("Claude... ", end="")
                    claude_response = run_claude_call(prompts[p])
                    diag, evals = process_response(claude_response)
                    start = df.columns.get_loc(f"CLAUDE_{p}_TanıVarYok")
                    df.iloc[i, start] = "Var" if diag else "Yok"
                    if diag:
                        df.iloc[i, start + 1:start + 4] = evals
            except Exception as e:
                print(f"exception occurred for {df.iloc[i, 1]}")
            print("done.")

    except Exception as e:
        print(e)
        print("ending early.")
        df.to_excel("<Temporary_Output_File>")
        exit()

    df.to_excel("<Output_File>")