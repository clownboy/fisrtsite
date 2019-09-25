from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
@csrf_exempt
@api_view(['POST'])
def noteonline(request):
    if request.method =='POST':
        notepic = request.GET['note']
        picurl = 'https://notepic-1259769191.cos.ap-shanghai.myqcloud.com/'+notepic
        try:
            cred = credential.Credential(settings.WX_OCR_SECRET_ID,settings.WX_OCR_SECRET_KEY)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "ocr.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)
            req = models.GeneralEfficientOCRRequest()
            params = '{"ImageUrl":"'+picurl+'"}'
            req.from_json_string(params)
            resp = client.GeneralEfficientOCR(req).TextDetections
            content=""
            for i in resp:
              content=content+str(i.DetectedText)
            print(content)
            return  JsonResponse(data=content,safe=False)
        except TencentCloudSDKException as err:
            return  JsonResponse(data=err.to_json_string(),safe=False)
