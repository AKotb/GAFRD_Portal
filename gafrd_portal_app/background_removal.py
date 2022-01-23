import cv2

file_name = r"F:\NARSS\Fishers_Project\GAFRD_Portal\gafrd_portal_app\static\model_results\FinalRestrictionModel.png"
src = cv2.imread(file_name, 1)
tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
b, g, r = cv2.split(src)
rgba = [b,g,r, alpha]
dst = cv2.merge(rgba,4)
cv2.imwrite(file_name, dst)