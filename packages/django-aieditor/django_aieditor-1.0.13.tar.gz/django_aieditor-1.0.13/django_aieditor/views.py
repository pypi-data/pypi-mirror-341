from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('file')
        if image:
            # 生成唯一文件名
            ext = os.path.splitext(image.name)[1]
            filename = f'{uuid.uuid4().hex}{ext}'
            
            # 保存文件
            path = default_storage.save(f'aieditor/images/{filename}', image)
            
            # 获取完整URL (使用storage的url方法)
            file_url = default_storage.url(path)
            
            # 返回AiEditor要求的格式
            return JsonResponse({
                'errorCode': 0,
                'data': {
                    'src': file_url,
                    'alt': image.name
                }
            })
    
    return JsonResponse({
        'errorCode': 1,
        'message': '上传失败'
    }) 