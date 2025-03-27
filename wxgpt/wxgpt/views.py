from django.shortcuts import render
import erniebot
import json
from django.http import JsonResponse
def index(request):
    return render(request, 'index.html')
def create(request):
    return render(request, 'create.html')
def ask(request):
    question = request.GET.get('question','')
    # 设置文心一言的相关参数
    erniebot.api_type = 'aistudio'
    erniebot.access_token = "2a14e181576d07e3874b914c630c0668410e39a9"
    model = 'ernie-3.5'
    # 将文本放在单个消息对象中，用空格分隔不同的文本段落
    message_content = "The task scenario is: I need you to refine the knowledge points I provide into four small modules to help me learn."\
                      "The best way to refine is to follow a good learning path, and you need to stand from the perspective of a teacher to help me learn the knowledge well."\
                      f"-对每个模块进行介绍，让读者能够直观的知道该模块的学习内容 我提供的知识点为：{question}"\
                      "- 示例json文件如下，参考它的格式：[{\"模块主题\":\"\",\"本模块内容简介\":\"\"},]"\
                      "- Strictly follow the format I provided "\
                      "- 每个模块的介绍在50个中文汉字左右。"\
                      "- The output is just pure JSON format, with no other descriptions."
    messages = [
        {
            'role': 'user',
            'top_p': '0.001',
            'content': message_content
        }
    ]
    # 调用文心一言回答问题
    response = erniebot.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    # 获取文心一言的回答
    answer = response.result

    try:
        json_start = answer.find("[")
        json_end = answer.rfind("]")
        if json_start != -1 and json_end != -1:
            json_content = answer[json_start:json_end+1]
            answer_dict = json.loads(json_content)
        else:
            answer_dict = {}
    except json.JSONDecodeError:
        answer_dict = {}

    model_titles = []
    for item in answer_dict:
        model_title = item.get("模块主题","")
        model_discription = item.get("本模块内容简介", "")
        print(model_title)
        print(model_discription)
        if  model_title and model_discription:
            model_titles.append({"模块主题": model_title,"本模块内容简介": model_discription})

    return JsonResponse(model_titles,safe=False)