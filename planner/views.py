from django.shortcuts import render

def home(request):

    if request.method == "POST":

        age = int(request.POST['age'])
        weight = float(request.POST['weight'])
        height = float(request.POST['height'])
        diet = request.POST['diet']

        bmi = weight / ((height / 100) ** 2)
        bmi = round(bmi, 2)

        if bmi > 25:
            status = "Overweight"
            advice = "You need to reduce weight."
            calories = "Follow a calorie deficit of 100 calories for one month with sufficient protein intake."

        elif bmi < 18.5:
            status = "Underweight"
            advice = "You need to bulk."
            calories = "Follow a calorie surplus of 100 calories for one month with sufficient protein intake."

        else:
            status = "Normal Weight"
            advice = "Your BMI is healthy."
            calories = "Maintain balanced nutrition and current calorie intake."

        context = {
            'age': age,
            'weight': weight,
            'height': height,
            'diet': diet,
            'bmi': bmi,
            'status': status,
            'advice': advice,
            'calories': calories,
        }

        return render(request, 'result.html', context)

    return render(request, 'home.html')