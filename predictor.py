import numpy as np

def predict_grade(results):
    percentages = []
    for r in results:
        percentage = (r.marks_obtained / r.total_marks) * 100
        percentages.append(percentage)

    avg = np.mean(percentages)

    # Trend sirf tab calculate karo jab 2 ya zyada results hon
    if len(percentages) >= 2:
        trend = np.polyfit(range(len(percentages)), percentages, 1)[0]
    else:
        trend = 0  # Sirf 1 result hai toh trend 0 rakho

    predicted_avg = avg + (trend * 2)
    predicted_avg = max(0, min(100, predicted_avg))

    if predicted_avg >= 90:
        grade = 'A+'
        message = 'Excellent! Keep it up and maintain this performance!'
    elif predicted_avg >= 80:
        grade = 'A'
        message = 'Great performance! A little more effort can get you an A+!'
    elif predicted_avg >= 70:
        grade = 'B'
        message = 'Good performance! Stay focused and aim higher!'
    elif predicted_avg >= 60:
        grade = 'C'
        message = 'Average performance. You need to work harder!'
    elif predicted_avg >= 50:
        grade = 'D'
        message = 'Poor performance. Risk of failing next semester!'
    else:
        grade = 'F'
        message = 'Critical situation. Please consult your teacher immediately!'

    return {
        'predicted_percentage': round(predicted_avg, 2),
        'predicted_grade': grade,
        'message': message,
        'current_avg': round(avg, 2),
        'trend': 'Improving ✅' if trend > 0 else 'Declining ⚠️'
    }