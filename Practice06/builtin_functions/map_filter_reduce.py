from functools import reduce


scores = ["85", "90", "46", "58", "88", "47"]

scores_int = list(map(int, scores))
print("Scores:", scores_int)


passed = list(filter(lambda x: x >= 50, scores_int))
print("Passed students:", passed)


total_score = reduce(lambda x, y: x + y, scores_int)
print("Total score:", total_score)
