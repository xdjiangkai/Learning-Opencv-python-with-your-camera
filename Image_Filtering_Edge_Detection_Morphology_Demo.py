import cv2
import sys
'''
使用方式：直接运行，运行后在键盘上按对应的功能建
----------------------------------------------
  功能键 | 功能
    Q   | 退出
    0   | 预览二值图像
    1   | 预览灰度图
    2   | 高斯滤波
    3   | 中值滤波
    4   | 双边滤波
    5   | 水平soble
    6   | 垂直sobel
    7   | 图像sobel梯度的振幅
    8   | 水平DerivativeOfGaussian滤波检测边缘
    9   | 水平LaplacianOfGaussian滤波检测边缘
    A   | 垂直DerivativeOfGaussian滤波检测边缘
    S   | 垂直LaplacianOfGaussian滤波检测边缘
    D   | DerivativeOfGaussian滤波检测边缘
    F   | LaplacianOfGaussian滤波检测边缘
    W   | 二值图像膨胀
    E   | 二值图像腐蚀 
    R   | 二值图像开操作
    T   | 二值图像闭操作
    Y   | 灰度图像膨胀
    U   | 灰度图像腐蚀 
    I   | 灰度图像开操作
    O   | 灰度图像闭操作
'''
print(
    '''
使用方式：直接运行，运行后在键盘上按对应的功能建
----------------------------------------------
  功能键 | 功能
    Q   | 退出
    0   | 预览二值图像
    1   | 预览灰度图
    2   | 高斯滤波
    3   | 中值滤波
    4   | 双边滤波
    5   | 水平soble
    6   | 垂直sobel
    7   | 图像sobel梯度的振幅
    8   | 水平DerivativeOfGaussian滤波检测边缘
    9   | 水平LaplacianOfGaussian滤波检测边缘
    A   | 垂直DerivativeOfGaussian滤波检测边缘
    S   | 垂直LaplacianOfGaussian滤波检测边缘
    D   | DerivativeOfGaussian滤波检测边缘
    F   | LaplacianOfGaussian滤波检测边缘
    W   | 二值图像膨胀
    E   | 二值图像腐蚀 
    R   | 二值图像开操作
    T   | 二值图像闭操作
    Y   | 灰度图像膨胀
    U   | 灰度图像腐蚀 
    I   | 灰度图像开操作
    O   | 灰度图像闭操作
'''
)
PREVIEW  = 0   # Preview Mode
PREVIEWBW = 1
GaussianBlur = 4 # GaussianBlur cv.GaussianBlur(src, ksize, sigmaX[, dst[, sigmaY[, borderType]]]	) ->	dst
MedianBlur = 5 # cv.medianBlur(src, ksize[, dst]	) ->	dst
BilateralFilter = 6 # cv.bilateralFilter(src, d, sigmaColor, sigmaSpace[, dst[, borderType]]	) ->	dst
SobelHorizon = 7 # cv.Sobel(	src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]]	) ->	dst
SobelVertical = 8
Magnitude = 9
DerivativeOfGaussianHorizon = 10
LaplacianOfGaussianHorizon  = 11
DilateBW = 12 # cv.dilate(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]	) ->	dst
ErodeBW = 13 # cv.erode(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]	) ->	dst
OpenBW = 14
CloseBW = 15

Dilate = 16 # cv.dilate(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]	) ->	dst
Erode = 17 # cv.erode(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]	) ->	dst
Open = 18
Close = 19

DerivativeOfGaussianVertical = 20
LaplacianOfGaussianVertical = 21

DerivativeOfGaussian = 22
LaplacianOfGaussian  = 23

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.2,
                       minDistance = 15,
                       blockSize = 9)
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

image_filter = PREVIEW
alive = True

win_name = 'Camera Filters'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
result = None

source = cv2.VideoCapture(s)

while alive:
    has_frame, frame = source.read()
    if not has_frame:
        break

    # frame = cv2.flip(frame,1)
    # 转化为灰度值
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    if image_filter == PREVIEW:
        result = frame
    if image_filter == PREVIEWBW:
        ret,result = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    elif image_filter == GaussianBlur:
        result = cv2.GaussianBlur(src=frame, ksize=(9,9), sigmaX=5, sigmaY=8)
    elif image_filter == MedianBlur: 
        result = cv2.medianBlur(src=frame, ksize=9)
    elif image_filter == BilateralFilter:
        result = cv2.bilateralFilter(src=frame, d=13,sigmaColor=29, sigmaSpace=29)
    elif image_filter == SobelHorizon:
        result = cv2.Sobel(src=frame, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3)
    elif image_filter == SobelVertical:
        result = cv2.Sobel(src=frame, ddepth=cv2.CV_8U, dx=0, dy=1, ksize=3)
    elif image_filter == Magnitude:
        resultHorizon = cv2.Sobel(src=frame, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3)
        resultVertical = cv2.Sobel(src=frame, ddepth=cv2.CV_8U, dx=0, dy=1, ksize=3)
        result = cv2.addWeighted(src1=resultHorizon, alpha=0.5, src2=resultVertical, beta=0.5, gamma=0)
    elif image_filter == DerivativeOfGaussianHorizon:
        result = cv2.GaussianBlur(src=frame, ksize=(5,5), sigmaX=3, sigmaY=3)
        result = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=0, dy=1, ksize=3)
    elif image_filter == LaplacianOfGaussianHorizon:
        result = cv2.GaussianBlur(src=frame, ksize=(5,5), sigmaX=3, sigmaY=3)
        result = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=0, dy=1, ksize=3)
        result = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=0, dy=1, ksize=3)
    elif image_filter == DerivativeOfGaussianVertical:
        result = cv2.GaussianBlur(src=frame, ksize=(5,5), sigmaX=3, sigmaY=3)
        result = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3)
    elif image_filter == LaplacianOfGaussianVertical:
        result = cv2.GaussianBlur(src=frame, ksize=(5,5), sigmaX=3, sigmaY=3)
        result = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3)
        result = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3)
    elif image_filter == DerivativeOfGaussian:
        result = cv2.GaussianBlur(src=frame, ksize=(5,5), sigmaX=3, sigmaY=3)
        resultHorizon = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=0, dy=1, ksize=3)
        result = cv2.GaussianBlur(src=frame, ksize=(5,5), sigmaX=3, sigmaY=3)
        resultVertical = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3)
        result = cv2.addWeighted(src1=resultHorizon, alpha=0.5, src2=resultVertical, beta=0.5, gamma=0)
    elif image_filter == LaplacianOfGaussian:
        result = cv2.GaussianBlur(src=frame, ksize=(5,5), sigmaX=3, sigmaY=3)
        result = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=0, dy=1, ksize=3)
        resultHorizon = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=0, dy=1, ksize=3)
        result = cv2.GaussianBlur(src=frame, ksize=(5,5), sigmaX=3, sigmaY=3)
        result = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3)
        resultVertical = cv2.Sobel(src=result, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3)
        result = cv2.addWeighted(src1=resultHorizon, alpha=0.5, src2=resultVertical, beta=0.5, gamma=0)
    elif image_filter == DilateBW:
        ret,result = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        result = cv2.dilate(src=result,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
    elif image_filter == ErodeBW:
        ret,result = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        result = cv2.erode(src=result,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
    elif image_filter == OpenBW:
        ret,result = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        result = cv2.erode(src=result,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
        result = cv2.dilate(src=result,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
    elif image_filter == CloseBW:
        ret,result = cv2.threshold(frame,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        result = cv2.dilate(src=result,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
        result = cv2.erode(src=result,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
    elif image_filter == Dilate:
        result = cv2.dilate(src=frame,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
    elif image_filter == Erode:
        result = cv2.erode(src=frame,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
    elif image_filter == Open:
        result = cv2.erode(src=frame,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
        result = cv2.dilate(src=result,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
    elif image_filter == Close:
        result = cv2.dilate(src=frame,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))
        result = cv2.erode(src=result,kernel=cv2.getStructuringElement(shape=cv2.MORPH_RECT,ksize=(10,10)))

    cv2.imshow(win_name, result)

    key = cv2.waitKey(1)
    if key == ord('Q') or key == ord('q') or key == 27:
        alive = False
    elif key == ord('0'):   
        image_filter = PREVIEWBW
    elif key == ord('1'):   
        image_filter = PREVIEW
    elif key == ord('2'):   
        image_filter = GaussianBlur
    elif key == ord('3'):   
        image_filter = MedianBlur
    elif key == ord('4'):   
        image_filter = BilateralFilter
    elif key == ord('5'):   
        image_filter = SobelHorizon
    elif key == ord('6'):   
        image_filter = SobelVertical
    elif key == ord('7'):   
        image_filter = Magnitude
    elif key == ord('8'):   
        image_filter = DerivativeOfGaussianHorizon
    elif key == ord('9'):   
        image_filter = LaplacianOfGaussianHorizon
    elif key == ord('W') or key == ord('w'):   
        image_filter = DilateBW
    elif key == ord('E') or key == ord('e'):    
        image_filter = ErodeBW
    elif key == ord('R') or key == ord('r'):   
        image_filter = OpenBW
    elif key == ord('T') or key == ord('t'):    
        image_filter = CloseBW
    elif key == ord('Y') or key == ord('y'):   
        image_filter = Dilate
    elif key == ord('U') or key == ord('u'):    
        image_filter = Erode
    elif key == ord('I') or key == ord('i'):   
        image_filter = Open
    elif key == ord('O') or key == ord('o'):    
        image_filter = Close
    elif key == ord('A') or key == ord('a'):  
        image_filter = DerivativeOfGaussianVertical
    elif key == ord('S') or key == ord('s'):  
        image_filter = LaplacianOfGaussianVertical
    elif key == ord('D') or key == ord('d'):  
        image_filter = DerivativeOfGaussian
    elif key == ord('F') or key == ord('f'):  
        image_filter = LaplacianOfGaussian
source.release()
cv2.destroyWindow(win_name)

def magnitude():
    pass
