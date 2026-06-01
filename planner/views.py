from django.shortcuts import render

FOOD_DB = {
    "rice": {
        "calories": 130, "protein": 2.5, "fiber": 0.4, "carbs": 28, "fat": 0.3,
        "vitamin_c": 0, "calcium": 10, "vitamin_b": 0.02, "probiotics": 0,
    },
    "cooked_dal": {
        "calories": 116, "protein": 9, "fiber": 8, "carbs": 20, "fat": 0.4,
        "vitamin_c": 2, "calcium": 19, "vitamin_b": 0.1, "probiotics": 0,
    },
    "paneer": {
        "calories": 265, "protein": 18, "fiber": 0, "carbs": 1.2, "fat": 20,
        "vitamin_c": 0, "calcium": 208, "vitamin_b": 0.1, "probiotics": 0,
    },
    "chicken": {
        "calories": 165, "protein": 31, "fiber": 0, "carbs": 0, "fat": 3.6,
        "vitamin_c": 0, "calcium": 15, "vitamin_b": 0.5, "probiotics": 0,
    },
    "egg": {
        "calories": 155, "protein": 13, "fiber": 0, "carbs": 1.1, "fat": 11,
        "vitamin_c": 0, "calcium": 50, "vitamin_b": 0.45, "probiotics": 0,
    },
    "whey_protein": {
        "calories": 400, "protein": 80, "fiber": 0, "carbs": 8, "fat": 6,
        "vitamin_c": 0, "calcium": 450, "vitamin_b": 0.2, "probiotics": 0,
    },
    "chia_seeds": {
        "calories": 486, "protein": 17, "fiber": 34, "carbs": 42, "fat": 31,
        "vitamin_c": 1, "calcium": 631, "vitamin_b": 0.1, "probiotics": 0,
    },
    "nuts": {
        "calories": 607, "protein": 20, "fiber": 8, "carbs": 21, "fat": 54,
        "vitamin_c": 0, "calcium": 269, "vitamin_b": 0.2, "probiotics": 0,
    },
    "isabgol": {
        "calories": 20, "protein": 0, "fiber": 80, "carbs": 0, "fat": 0,
        "vitamin_c": 0, "calcium": 0, "vitamin_b": 0, "probiotics": 0,
    },
    "mixed_vegetable_curry": {
        "calories": 90, "protein": 3, "fiber": 6, "carbs": 12, "fat": 3,
        "vitamin_c": 35, "calcium": 40, "vitamin_b": 0.1, "probiotics": 0,
    },
    "curd": {
        "calories": 98, "protein": 11, "fiber": 0, "carbs": 3.4, "fat": 4.3,
        "vitamin_c": 1, "calcium": 121, "vitamin_b": 0.2, "probiotics": 1,
    },
    "buttermilk": {
        "calories": 40, "protein": 3, "fiber": 0, "carbs": 5, "fat": 1,
        "vitamin_c": 1, "calcium": 116, "vitamin_b": 0.1, "probiotics": 1,
    },
}


def calc_by_grams(food_key, grams):
    item = FOOD_DB[food_key]
    scale = grams / 100
    return {
        "food": food_key.replace("_", " ").title(),
        "grams": round(grams, 1),
        "calories": round(item["calories"] * scale, 2),
        "protein": round(item["protein"] * scale, 2),
        "fiber": round(item["fiber"] * scale, 2),
        "carbs": round(item["carbs"] * scale, 2),
        "fat": round(item["fat"] * scale, 2),
        "vitamin_c": round(item["vitamin_c"] * scale, 2),
        "calcium": round(item["calcium"] * scale, 2),
        "vitamin_b": round(item["vitamin_b"] * scale, 2),
        "probiotics": round(item["probiotics"] * scale, 2),
    }


def calc_by_protein(food_key, protein_target):
    item = FOOD_DB[food_key]
    grams = 20 if item["protein"] == 0 else (protein_target / item["protein"]) * 100
    return calc_by_grams(food_key, grams)


def sum_meal(items):
    totals = {
        "total_calories": 0, "total_protein": 0, "total_fiber": 0,
        "total_carbs": 0, "total_fat": 0, "total_vitamin_c": 0,
        "total_calcium": 0, "total_vitamin_b": 0, "total_probiotics": 0
    }
    for item in items:
        totals["total_calories"]  += item["calories"]
        totals["total_protein"]   += item["protein"]
        totals["total_fiber"]     += item["fiber"]
        totals["total_carbs"]     += item["carbs"]
        totals["total_fat"]       += item["fat"]
        totals["total_vitamin_c"] += item["vitamin_c"]
        totals["total_calcium"]   += item["calcium"]
        totals["total_vitamin_b"] += item["vitamin_b"]
        totals["total_probiotics"]+= item["probiotics"]
    totals = {k: round(v, 2) for k, v in totals.items()}
    totals["items"] = items
    return totals

def home(request):
    if request.method == "POST":
        age    = int(request.POST["age"])
        weight = float(request.POST["weight"])
        height = float(request.POST["height"])
        diet   = request.POST["diet"]

        bmi = round(weight / ((height / 100) ** 2), 2)

        if bmi < 18.5:
            status = "Underweight"
            advice = "Increase healthy calories and proteins."
        elif bmi > 25:
            status = "Overweight"
            advice = "Protein priority with controlled carbs."
        else:
            status = "Normal"
            advice = "Balanced high-protein nutrition."

        calorie_target    = round(weight * 30 - (100 if bmi > 25 else 0), 2)
        protein_target    = round(weight * 1.8, 2)
        fiber_target      = round(weight * 0.35, 2)
        vitamin_c_target  = 90
        calcium_target    = 1000
        vitamin_b_target  = 1.3
        probiotics_target = 3

        breakfast_protein = protein_target * 0.30
        lunch_protein     = protein_target * 0.40
        dinner_protein    = protein_target * 0.30

        if diet == "veg":
            b_whey   = calc_by_protein("whey_protein", breakfast_protein * 0.55)
            b_paneer = calc_by_protein("paneer",        breakfast_protein * 0.35)
            b_chia   = calc_by_grams("chia_seeds", 15)
            b_nuts   = calc_by_grams("nuts", 20)
            b_curd   = calc_by_grams("curd", 150)
            breakfast_items = [b_whey, b_paneer, b_chia, b_nuts, b_curd]

            l_paneer = calc_by_protein("paneer",       lunch_protein * 0.40)
            l_dal    = calc_by_protein("cooked_dal",   lunch_protein * 0.35)
            l_whey   = calc_by_protein("whey_protein", lunch_protein * 0.15)
            l_veg    = calc_by_grams("mixed_vegetable_curry", 150)
            l_butter = calc_by_grams("buttermilk", 200)
            committed = sum(x["calories"] for x in [l_paneer, l_dal, l_whey, l_veg, l_butter])
            remaining = max(calorie_target * 0.35 - committed, 0)
            rice_grams = max(50, min(round((remaining / FOOD_DB["rice"]["calories"]) * 100, 1), 200))
            l_rice = calc_by_grams("rice", rice_grams)
            lunch_items = [l_paneer, l_dal, l_whey, l_rice, l_veg, l_butter]

            d_whey = calc_by_protein("whey_protein", dinner_protein * 0.50)
            d_dal  = calc_by_protein("cooked_dal",   dinner_protein * 0.35)
            d_veg  = calc_by_grams("mixed_vegetable_curry", 150)
            d_isab = calc_by_grams("isabgol", 10)
            d_curd = calc_by_grams("curd", 100)
            dinner_items = [d_whey, d_dal, d_veg, d_isab, d_curd]

        else:
            b_whey = calc_by_protein("whey_protein", breakfast_protein * 0.45)
            b_egg  = calc_by_protein("egg",           breakfast_protein * 0.40)
            b_chia = calc_by_grams("chia_seeds", 15)
            b_nuts = calc_by_grams("nuts", 20)
            b_curd = calc_by_grams("curd", 150)
            breakfast_items = [b_whey, b_egg, b_chia, b_nuts, b_curd]

            l_chicken = calc_by_protein("chicken",      lunch_protein * 0.45)
            l_dal     = calc_by_protein("cooked_dal",   lunch_protein * 0.25)
            l_whey    = calc_by_protein("whey_protein", lunch_protein * 0.15)
            l_veg     = calc_by_grams("mixed_vegetable_curry", 150)
            l_butter  = calc_by_grams("buttermilk", 200)
            committed = sum(x["calories"] for x in [l_chicken, l_dal, l_whey, l_veg, l_butter])
            remaining = max(calorie_target * 0.35 - committed, 0)
            rice_grams = max(50, min(round((remaining / FOOD_DB["rice"]["calories"]) * 100, 1), 200))
            l_rice = calc_by_grams("rice", rice_grams)
            lunch_items = [l_chicken, l_dal, l_whey, l_rice, l_veg, l_butter]

            d_egg  = calc_by_protein("egg",          dinner_protein * 0.40)
            d_whey = calc_by_protein("whey_protein", dinner_protein * 0.40)
            d_veg  = calc_by_grams("mixed_vegetable_curry", 150)
            d_isab = calc_by_grams("isabgol", 10)
            d_curd = calc_by_grams("curd", 100)
            dinner_items = [d_egg, d_whey, d_veg, d_isab, d_curd]

        breakfast = sum_meal(breakfast_items)
        lunch     = sum_meal(lunch_items)
        dinner    = sum_meal(dinner_items)

        # Sentence summaries
        if diet == "veg":
            breakfast_sentence = (
                f"Breakfast: {int(b_whey['grams'])}g of WHEY PROTEIN shake with "
                f"{int(b_paneer['grams'])}g of PANEER, "
                f"15g of CHIA SEEDS, 20g of NUTS, "
                f"and 150g of CURD."
            )
            lunch_sentence = (
                f"Lunch: {int(l_rice['grams'])}g of RICE with "
                f"{int(l_paneer['grams'])}g of PANEER, "
                f"{int(l_dal['grams'])}g of COOKED DAL, "
                f"a scoop ({int(l_whey['grams'])}g) of WHEY PROTEIN, "
                f"150g of MIXED VEGETABLE CURRY, "
                f"and a glass (200g) of BUTTERMILK."
            )
            dinner_sentence = (
                f"Dinner: {int(d_whey['grams'])}g of WHEY PROTEIN shake with "
                f"{int(d_dal['grams'])}g of COOKED DAL, "
                f"150g of MIXED VEGETABLE CURRY, "
                f"1 tsp (10g) of ISABGOL mixed in water, "
                f"and 100g of CURD."
            )
        else:
            breakfast_sentence = (
                f"Breakfast: {int(b_whey['grams'])}g of WHEY PROTEIN shake with "
                f"{int(b_egg['grams'])}g of EGGS, "
                f"15g of CHIA SEEDS, 20g of NUTS, "
                f"and 150g of CURD."
            )
            lunch_sentence = (
                f"Lunch: {int(l_rice['grams'])}g of RICE with "
                f"{int(l_chicken['grams'])}g of CHICKEN, "
                f"{int(l_dal['grams'])}g of COOKED DAL, "
                f"a scoop ({int(l_whey['grams'])}g) of WHEY PROTEIN, "
                f"150g of MIXED VEGETABLE CURRY, "
                f"and a glass (200g) of BUTTERMILK."
            )
            dinner_sentence = (
                f"Dinner: {int(d_egg['grams'])}g of EGGS with "
                f"{int(d_whey['grams'])}g of WHEY PROTEIN shake, "
                f"150g of MIXED VEGETABLE CURRY, "
                f"1 tsp (10g) of ISABGOL mixed in water, "
                f"and 100g of CURD."
            )

        # Full descriptions
        if diet == "veg":
            lunch_description = (
                f"This lunch is built around paneer ({round(l_paneer['protein'], 1)}g protein) and cooked dal "
                f"({round(l_dal['protein'], 1)}g protein — cooked values, not raw). A whey protein scoop tops up "
                f"the meal to meet your {round(lunch_protein, 1)}g lunch protein target. Rice ({int(rice_grams)}g) "
                f"fills the remaining calories as complex carbs, calculated only after accounting for all protein "
                f"and micronutrient calories. Mixed vegetable curry adds {round(l_veg['fiber'], 1)}g fibre and "
                f"{round(l_veg['vitamin_c'], 1)}mg Vitamin C. Buttermilk provides {round(l_butter['calcium'], 1)}mg "
                f"calcium and covers probiotics for this meal."
            )
            dinner_description = (
                f"This dinner focuses on recovery and gut health. Whey protein ({int(d_whey['grams'])}g) and cooked "
                f"dal ({int(d_dal['grams'])}g) deliver {round(dinner['total_protein'], 1)}g protein for overnight "
                f"muscle repair. Carbs are kept minimal. Mixed vegetable curry adds {round(d_veg['fiber'], 1)}g fibre "
                f"and {round(d_veg['vitamin_c'], 1)}mg Vitamin C. Isabgol (10g psyllium husk) boosts gut fibre and "
                f"bowel regularity. Curd closes the meal with {round(d_curd['calcium'], 1)}mg calcium and a probiotic serving."
            )
        else:
            lunch_description = (
                f"This lunch leads with chicken ({round(l_chicken['protein'], 1)}g protein) — lean and highly "
                f"bioavailable. Cooked dal adds {round(l_dal['protein'], 1)}g protein plus fibre (cooked values used). "
                f"A whey protein scoop tops up to your {round(lunch_protein, 1)}g lunch target. Rice ({int(rice_grams)}g) "
                f"provides remaining calories as carbs, added only after subtracting protein and micronutrient calories. "
                f"Mixed vegetable curry delivers {round(l_veg['fiber'], 1)}g fibre and {round(l_veg['vitamin_c'], 1)}mg "
                f"Vitamin C. Buttermilk adds {round(l_butter['calcium'], 1)}mg calcium and probiotics."
            )
            dinner_description = (
                f"This dinner combines eggs ({int(d_egg['grams'])}g) and whey protein ({int(d_whey['grams'])}g) for "
                f"{round(dinner['total_protein'], 1)}g total protein to support overnight recovery. Carbs are "
                f"intentionally minimal. Mixed vegetable curry provides {round(d_veg['fiber'], 1)}g fibre and "
                f"{round(d_veg['vitamin_c'], 1)}mg Vitamin C. Isabgol (10g) supports gut motility and microbiome health. "
                f"Curd gives {round(d_curd['calcium'], 1)}mg calcium and a probiotic dose to end the day."
            )

        context = {
            "age": age, "weight": weight, "height": height, "diet": diet,
            "bmi": bmi, "status": status, "advice": advice,
            "calorie_target": calorie_target, "protein_target": protein_target,
            "fiber_target": fiber_target, "vitamin_c_target": vitamin_c_target,
            "calcium_target": calcium_target, "vitamin_b_target": vitamin_b_target,
            "probiotics_target": probiotics_target,
            "breakfast": breakfast, "lunch": lunch, "dinner": dinner,
            "breakfast_sentence": breakfast_sentence,
            "lunch_sentence": lunch_sentence,
            "dinner_sentence": dinner_sentence,
            "lunch_description": lunch_description,
            "dinner_description": dinner_description,
        }

        return render(request, "result.html", context)

    return render(request, "home.html")