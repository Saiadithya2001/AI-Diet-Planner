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


def scale_food(food, protein_target):
    item = FOOD_DB[food]

    scale = protein_target / item["protein"] if item["protein"] != 0 else 1

    grams = round(scale * 100, 2)

    return {
        "food": food,
        "grams": grams,
        "calories": round(item["calories"] * scale, 2),
        "protein": round(item["protein"] * scale, 2),
        "fiber": round(item["fiber"] * scale, 2),
    }


def home(request):

    if request.method == "POST":

        age = int(request.POST["age"])
        weight = float(request.POST["weight"])
        height = float(request.POST["height"])
        diet = request.POST["diet"]

        bmi = weight / ((height / 100) ** 2)
        bmi = round(bmi, 2)

        protein_target = weight * 1.5

        if bmi < 18.5:
            status = "Underweight"
            calorie_target = weight * 35
            advice = "Increase calorie intake (bulk diet)."

        elif bmi > 25:
            status = "Overweight"
            calorie_target = weight * 25
            advice = "Follow calorie deficit diet."

        else:
            status = "Normal"
            calorie_target = weight * 30
            advice = "Maintain balanced diet."

        fiber_target = weight * 0.3

        if diet == "veg":
            breakfast_food = "oats"
            lunch_food = "dal"
            dinner_food = "paneer"
        else:
            breakfast_food = "egg"
            lunch_food = "chicken"
            dinner_food = "egg"

        breakfast = scale_food(breakfast_food, protein_target / 3)
        lunch = scale_food(lunch_food, protein_target / 3)
        dinner = scale_food(dinner_food, protein_target / 3)

        context = {
            "age": age,
            "weight": weight,
            "height": height,
            "diet": diet,
            "bmi": bmi,
            "status": status,
            "advice": advice,
            "calorie_target": round(calorie_target, 2),
            "protein_target": round(protein_target, 2),
            "fiber_target": round(fiber_target, 2),
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
        }

        return render(request, "result.html", context)

    return render(request, "home.html")