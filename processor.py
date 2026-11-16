def build_prompt(base, row):
    base = base.replace("<2>", str(row["Yaş?"]))
    base = base.replace("<3>", row["Cinsiyet?"])

    prompt_1 = base
    prompt_1 = (prompt_1.replace("<1>", "Çocuk")
                .replace("<4>", row["Çocuk tam öykü?"] if row["Çocuk tam öykü?"] != "" else "YOK"))

    prompt_2 = base
    prompt_2 = (prompt_2.replace("<1>", "Ebeveyn")
                .replace("<4>", row["Aile tam öykü?"] if row["Aile tam öykü?"] != "" else "YOK"))

    prompt_3 = base
    prompt_3 = (prompt_3.replace("<1>", "Çocuk + Ebeveyn")
                .replace("<4>", f"{row["Çocuk tam öykü?"]}\n{row["Aile tam öykü?"]}"))

    prompt_4 = base
    prompt_4 = (prompt_4.replace("<1>", "Çocuk + Ebeveyn + Hekim Muayenesi")
                .replace("<4>", row["Tüm anamnez (RDM + Aile + çocuk öyküsü)"]))

    return {"Çocuk": prompt_1, "Ebeveyn": prompt_2, "Çocuk + Ebeveyn": prompt_3, "Çocuk + Ebeveyn + Hekim Muayenesi": prompt_4}


def process_response(response):
    search_str = "2. En olası klinik değerlendirmeler:"
    diag, evals = False, []
    find_diag = response.find(search_str)
    if len(response[find_diag:]) > len(search_str) + 5:
        evals_str = response[find_diag+len(search_str):]
        find_1, find_2, find_3 = evals_str.find("1."), evals_str.find("2."), evals_str.find("3.")
        eval_1, eval_2, eval_3 = evals_str[find_1:find_2], evals_str[find_2:find_3], evals_str[find_3:]
        evals = [eval_1, eval_2, eval_3]
        diag = True
    return diag, evals