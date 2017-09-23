from django.shortcuts import render
from django.template import loader
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.http import HttpResponse


import json


# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def accept_temp(request):
	if request.method=='POST':
		template=json.loads(request.POST["template"])
		questions=[]
		for question in template["questions"]:
			questions.append(question)
			request.session["questions"]=questions
			request.session["stage"]=0
			request.session["variables"]=[]
		"""
		return render(request,"chat_page.html")
		"""
		return redirect("chat_page")
	else:
		return render(request,'accept_temp.html')

def chat_page(request):
	if request.method=='POST':

		questions=request.session["questions"]
		print(request.session["stage"])
		
		length_of_conv=len(request.session["questions"])
		while request.session["stage"] < length_of_conv:


			if "list_var" in questions[request.session["stage"]]:
				answer=""
				
				
				request.session["instruction_var"]=questions[request.session["stage"]]["instruction_var"]
				print(request.session["instruction_var"])
				#for key in request.session["variables"]:
				#	print(key)
				for j in range(len(request.session["instruction_var"])):
					if request.session["variables"][-1] in request.session["instruction_var"][j]:

						request.session["instruction_var"][j]=request.session["instruction_var"][j].replace(request.session["variables"][-1],"request.session[request.session['variables'][-1]]")
				for i in range(len(questions[request.session["stage"]]["instruction_var"])+1):
					ins_var=questions[request.session["stage"]]["instruction_var"]
					ins_var_eval=[]

					print(ins_var)
					print(questions[request.session["stage"]]["instruction_var"])
					for p in range(len(ins_var)):
						
						ins_var_eval.append(eval(ins_var[p]))
					print(questions[request.session["stage"]]["instruction_var"])
					questions[request.session["stage"]]["instruction"]=questions[request.session["stage"]]["instruction"].replace("%s","{}")

					answer=answer+"".join(questions[request.session["stage"]]["instruction"].format(*ins_var_eval))


				return render(request,"chat_page.html",{"answer":answer})







					

			
			if "conditions" in questions[request.session["stage"]]:
				request.session[request.session["variables"][-1]]=request.POST["message"]
				for cond in questions[request.session["stage"]]["conditions"]:
					cond_copy=cond[0]
					cond_copy=cond_copy.replace(request.session["previous_var"],"request.session[request.session['variables'][-1]]")
					
					if not eval(cond_copy):
						questions[request.session["stage"]]["var"]=request.POST["message"]
						request.session["stage"]=request.session["stage"]+1
						
						continue

					else:
						return render(request,"chat_page.html",{"answer":questions[request.session["stage"]]["text"]})

		
			if "instruction" in questions[request.session["stage"]]:

				if "instruction_var" in questions[request.session["stage"]]:
					questions[request.session["stage"]]["instruction"]=questions[request.session["stage"]]["instruction"].replace("%s","{}")
					instruction_variable=questions[request.session["stage"]]['instruction_var'][0]
					

					answer=questions[request.session["stage"]]["instruction"].format(request.session[instruction_variable])
					content = render_to_string("chat_page.html",{"answer":answer}, request=request)
					response=HttpResponse(content)
					request.session["stage"]=request.session["stage"]+1
					return response
					

				else:
					answer=questions[request.session["stage"]]["instruction"] + "\n(Press Send to continue)"
					content = render_to_string("chat_page.html",{"answer":answer}, request=request)
					response=HttpResponse(content)
					request.session["stage"]=request.session["stage"]+1
					return response


		
				

			if "text" in questions[request.session["stage"]]:

				answer=questions[request.session["stage"]]["text"]
				del questions[request.session["stage"]]["text"]
				if "options" in questions[request.session["stage"]]:
					opt_string=""
					for opt in questions[request.session["stage"]]["options"]:
						opt_string=opt_string+"/"+opt

					del questions[request.session["stage"]]["options"]
					answer=answer+" "+opt_string
					return render(request,"chat_page.html",{"answer":answer})
					
				else:
					return render(request,"chat_page.html",{"answer":answer})
			
			if "calculated_variable" in questions[request.session["stage"]]:
				
				formula_value=eval(questions[request.session["stage"]]["formula"],dict(request.session))
				print(formula_value)
				request.session[questions[request.session["stage"]]["var"]]=formula_value
				variable_name=questions[request.session["stage"]]["var"]
				request.session["variables"].append(variable_name)
				request.session["stage"]=request.session["stage"]+1
				continue

				


			
			
				

				
				

			if "var" in questions[request.session["stage"]] and "calculated_variable" not in questions[request.session["stage"]]:
				
				variable_name=questions[request.session["stage"]]["var"]
				request.session["variables"].append(variable_name)
				request.session["previous_var"]=variable_name
				exec('questions[request.session["stage"]]["var"] = request.POST["message"]')
				questions[request.session["stage"]][variable_name]=questions[request.session["stage"]].pop('var')
				print(questions[request.session["stage"]])
				for key,val in questions[request.session["stage"]].items():
					request.session[key]=val

				
				request.session["stage"]=request.session["stage"]+1
				continue
	else:
		questions=request.session["questions"]
		if "instruction" in questions[request.session["stage"]]:

			answer=questions[request.session["stage"]]["instruction"] + "\n(Press Send to continue)"
			content = render_to_string("chat_page.html",{"answer":answer}, request=request)

				
			response=HttpResponse(content)
			request.session["stage"]=request.session["stage"]+1
			return response


				







		
		