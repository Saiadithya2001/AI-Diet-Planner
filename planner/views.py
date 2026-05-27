from django.shortcuts import render

FOOD_DB = {
    "rice": {"calories": 130, "protein": 2.5, "fiber": 0.4},
    "oats": {"calories": 389, "protein": 16.9, "fiber": 10.6},
    "milk": {"calories": 64, "protein": 3.3, "fiber": 0},
    "dal": {"calories": 116, "protein": 9, "fiber": 8},
    "paneer": {"calories": 265, "protein": 18, "fiber": 0},
    "egg": {"calories": 155, "protein": 13, "fiber": 0},
    "chicken": {"calories": 165, "protein": 31, "fiber": 0},
    "banana": {"calories": 89, "protein": 1.1, "fiber": 2.6},
    "chapati": {"calories": 110, "protein": 3, "fiber": 2.7},
}


def calculate_food(food, target_calories):

    item = FOOD_DB[food]

    scale = target_calories / item["calories"]

    grams = round(scale * 100, 2)

    return {
        "food": food.title(),
        "grams": grams,
        "calories": round(item["calories"] * scale, 2),
        "protein": round(item["protein"] * scale, 2),
        "fiber": round(item["fiber"] * scale, 2),
    }


def create_meal(food_items):

    total_calories = 0
    total_protein = 0
    total_fiber = 0

    for item in food_items:
        total_calories += item["calories"]
        total_protein += item["protein"]
        total_fiber += item["fiber"]

    return {
        "items": food_items,
        "total_calories": round(total_calories, 2),
        "total_protein": round(total_protein, 2),
        "total_fiber": round(total_fiber, 2),
    }


def home(request):

    if request.method == "POST":

        age = int(request.POST["age"])
        weight = float(request.POST["weight"])
        height = float(request.POST["height"])
        diet = request.POST["diet"]

        bmi = weight / ((height / 100) ** 2)
        bmi = round(bmi, 2)

        calorie_target = weight * 30

        if bmi > 25:
            calorie_target -= 100

        calorie_target = round(calorie_target, 2)

        protein_target = round(weight * 1.5, 2)
        fiber_target = round(weight * 0.3, 2)

        if bmi < 18.5:
            status = "Underweight"
            advice = "Increase healthy calorie intake."

        elif bmi > 25:
            status = "Overweight"
            advice = "Calorie deficit activated."

        else:
            status = "Normal"
            advice = "Balanced nutrition recommended."

        breakfast_calories = calorie_target * 0.25
        lunch_calories = calorie_target * 0.50
        dinner_calories = calorie_target * 0.25

        # VEG PLAN

        if diet == "veg":

            breakfast_items = [
                calculate_food("oats", breakfast_calories * 0.7),
                calculate_food("milk", breakfast_calories * 0.3),
            ]

            lunch_items = [
                calculate_food("rice", lunch_calories * 0.5),
                calculate_food("dal", lunch_calories * 0.3),
                calculate_food("paneer", lunch_calories * 0.2),
            ]

            dinner_items = [
                calculate_food("chapati", dinner_calories * 0.5),
                calculate_food("dal", dinner_calories * 0.3),
                calculate_food("paneer", dinner_calories * 0.2),
            ]

        # NON VEG PLAN

        else:

            breakfast_items = [
                calculate_food("egg", breakfast_calories * 0.6),
                calculate_food("milk", breakfast_calories * 0.4),
            ]

            lunch_items = [
                calculate_food("rice", lunch_calories * 0.4),
                calculate_food("chicken", lunch_calories * 0.4),
                calculate_food("dal", lunch_calories * 0.2),
            ]

            dinner_items = [
                calculate_food("chapati", dinner_calories * 0.5),
                calculate_food("egg", dinner_calories * 0.3),
                calculate_food("milk", dinner_calories * 0.2),
            ]

        breakfast = create_meal(breakfast_items)
        lunch = create_meal(lunch_items)
        dinner = create_meal(dinner_items)

        context = {
            "age": age,
            "weight": weight,
            "height": height,
            "diet": diet,
            "bmi": bmi,
            "status": status,
            "advice": advice,
            "calorie_target": calorie_target,
            "protein_target": protein_target,
            "fiber_target": fiber_target,
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
        }

        return render(request, "result.html", context)

    return render(request, "home.html")