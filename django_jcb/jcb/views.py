# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import re,json,os
from django.contrib.sessions.models import Session
import pyodbc

def main_page(request):
	return render_to_response('main.html',None)

def cs_page(request):
	dic1={}
	dic2={}
	dic3={}
	conn=pyodbc.connect('DRIVER={SQL Server};SERVER=12.31.0.29;DATABASE=jcb;UID=sa;PWD=Ceb4321')
	cur=conn.cursor()
	cur.execute('select * from cunkuanFTP;')
	result1=cur.fetchall()
	cur.execute('select * from daikuanFTP;')
	result2=cur.fetchall()
	cur.execute('select * from bb;')
	result3=cur.fetchall()
	for row in result1:
		dic1[row[0]]=str(row.FTP)
	for row in result2:
		dic2[row[0]]=str(row.FTP)
	for row in result3:
		dic3[row[3]]=str(row[2]).replace(' ','')
	#print json.dumps(dic3)
	#print json.dumps(dic1)
	rate=cur.execute('select rate from rate;').fetchone()[0]
	variables=RequestContext(request,{
		'item_count':range(1,21),
		'dic1':json.dumps(dic1),
		'dic2':json.dumps(dic2),
		'dic3':json.dumps(dic3),
		'rate':rate,
	})
	return render_to_response('cs.html',variables)

def xg_page(request,id):
	dic1={}
	dic2={}
	dic3={}
	conn=pyodbc.connect('DRIVER={SQL Server};SERVER=12.31.0.29;DATABASE=jcb;UID=sa;PWD=Ceb4321')
	cur=conn.cursor()
	cur.execute('select * from cunkuanFTP;')
	result1=cur.fetchall()
	cur.execute('select * from daikuanFTP;')
	result2=cur.fetchall()
	cur.execute('select * from bb;')
	result3=cur.fetchall()
	for row in result1:
		dic1[row[0]]=str(row.FTP)
	for row in result2:
		dic2[row[0]]=str(row.FTP)
	for row in result3:
		dic3[row[3]]=str(row[2]).replace(' ','')
	#print json.dumps(dic1)
	start=None
	end=None
	if request.GET.has_key('start') and request.GET.has_key('end'):
		start=request.GET['start']
		end=request.GET['end']
	rate=cur.execute('select rate from rate;').fetchone()[0]
	variables=RequestContext(request,{
		'item_count':range(1,21),
		'dic1':json.dumps(dic1),
		'dic2':json.dumps(dic2),
		'dic3':json.dumps(dic3),
		'id':id,
		'rate':rate,
		'start':start,
		'end':end
	})
	return render_to_response('xg.html',variables)

def gz_page(request):
	return render_to_response('gz.html',None)

@csrf_exempt
def wh_page(request):
	return render_to_response('wh.html',None)

@csrf_exempt
def wh_ftp_page(request):
	if request.method!='POST':
		response=HttpResponse("Method not allowed")
		response.status_code=405
		return response
	file=request.FILES.get('up',None)
	if file==None:
		response=HttpResponse('Conflict')
		response.status_code=409
		return response
	
	text=file.read()
	text=text.split('\r\n')[1:]
	conn=pyodbc.connect('DRIVER={SQL Server};SERVER=12.31.0.29;DATABASE=jcb;UID=sa;PWD=Ceb4321')
	cur=conn.cursor()
	cur.execute('delete from cunkuanFTP;')
	conn.commit()
	cur.execute('delete from daikuanFTP;')
	conn.commit()

	for item in text:
		item=item.split(',')
		if item=='':
			break
		day=item[0].replace(' ','')
		if day=='':
			break
		ck=item[1].replace(' ','').replace('%','')
		dk=item[2].replace(' ','').replace('%','')
		
		if ck!='':
			#print item
			#print day
			#print ck
			cur.execute('INSERT INTO cunkuanFTP VALUES(%d,%.6f);'%(int(day),float(ck)))
		if dk!='':
			#print item
			#print day
			#print dk
			cur.execute('INSERT INTO daikuanFTP VALUES(%d,%.6f);'%(int(day),float(dk)))
	conn.commit()

	conn.close()
	response=HttpResponse('<script type="text/javascript">alert("提交成功");window.location.href="/wh/";</script>')
	response.status_code=200
	return response

import re
from datetime import datetime
@csrf_exempt
def records_page(request):
	conn=pyodbc.connect('DRIVER={SQL Server};SERVER=12.31.0.29;DATABASE=jcb;UID=sa;PWD=Ceb4321')
	cur=conn.cursor()
	if request.method=='POST':
		data=str(request.raw_post_data).replace(',}','}')
		data=json.loads(data)
		if data['cust_name'].replace(' ','')=='':
			response=HttpResponse('Conflict')
			response.status_code=409
			return response
		bb={}
		cur.execute('select * from bb')
		rows=cur.fetchall()
		for row in rows:
			bb[row[3]]=float(row[2])
		num=cur.execute('select	max(id) from kehu where substring(id,1,8)=\''+datetime.now().strftime("%Y%m%d")+'\'').fetchone()[0]
		if num is None:
			num=0
		else:
			num=int(num[-4:])
		try:
			cur.execute('insert into kehu(cust_name,acct_no,amt,bb,fk_date,fk_qx,dk_rate,dk_profit,ftp,risk_assets,org,employee,middle_price,id,sffd,ypje,ypts,ypfxzc,ypsxfsr) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data['cust_name'],data['acct_no'],data['amt'],data['bb'],data['fk_date'],data['fk_qx'],data['dk_rate'],data['dk_profit'],data['ftp'],data['risk_assets'],data['org'],data['employee'],bb[data['bb']],datetime.now().strftime("%Y%m%d")+'%04d'%(num+1),data['sffd'],data['ypje'],data['ypts'],data['ypfxzc'],data['ypsxfsr'])
			conn.commit()
		except:
			response=HttpResponse('Conflict')
			response.status_code=409
			return response
		for i in range(1,21):
			if not data.has_key('ck_cust_name'+str(i)):
				break
			cur.execute('insert into cltj(acct_no,ck_cust_name,ck_acct_no,ck_avg_day,bb,ck_qx,ck_rate,ftp,ck_profit,org,zjywsr,other_cond,middle_price,index_no,id,psl) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data['acct_no'],data['ck_cust_name'+str(i)],data['ck_acct_no'+str(i)],data['ck_avg_day'+str(i)],data['bb'+str(i)],data['ck_qx'+str(i)],data['ck_rate'+str(i)],data['ftp'+str(i)],data['ck_profit'+str(i)],data['org'+str(i)],data['zjywsr'+str(i)],data['other_cond'+str(i)],bb[data['bb'+str(i)]],i,datetime.now().strftime("%Y%m%d")+'%04d'%(num+1),data['psl'+str(i)])
			conn.commit()

		conn.close()
		response=HttpResponse('{"num":'+datetime.now().strftime("%Y%m%d")+'%04d'%(num+1)+'}',mimetype="application/json")
		response.status_code=201
		return response
	elif request.method=='GET':
		if not request.GET.has_key('start') or not request.GET.has_key('end') or not request.GET.has_key('page'):
			return render_to_response('records.html',None)
		start=request.GET['start']
		end=request.GET['end']
		page=request.GET['page']
		if start is None or end is None or page is None:
			return render_to_response('records.html',None)
		if int(page)==0:
			response=HttpResponse('<script type="text/javascript">alert("已是首页");window.location.href=\'/records/?start='+str(start)+'&end='+str(end)+'&page=1\'</script>')
			response.status_code=200
			return response
		rows=cur.execute('select * from kehu where fk_date>=\''+start+'\' and fk_date<=\''+end+'\' order by fk_date').fetchall()[(int(page)-1)*30:int(page)*30]
		conn.close()
		if rows==[] and str(page)!='1':
			response=HttpResponse('<script type="text/javascript">alert("已是末页");window.location.href=\'/records/?start='+str(start)+'&end='+str(end)+'&page='+str(int(page)-1)+'\'</script>')
			response.status_code=200
			return response
		elif rows==[] and str(page)=='1':
			response=HttpResponse('<script type="text/javascript">alert("无相关结果");window.parent.location.href=\'/records/\'</script>')
			response.status_code=200
			return response
		s='<table><tr style=\'background-color:#999;\'><td width=150px>放款账号</td><td width=100px>放款日期</td><td width=300px>客户名称</td><td width=100px>金额</td></tr>'
		i=0
		for row in rows:
			if i%2==0:
				s+='<tr  style="cursor:pointer" onClick="window.location.href=\'/xg/id='+row.id+'/?start='+str(start)+'&end='+str(end)+'\'">'
			else:
				s+='<tr style=\'background-color:#999;cursor:pointer;\' onClick="window.location.href=\'/xg/id='+row.id+'/?start='+str(start)+'&end='+str(end)+'\'">'
			s+='<td>'+row.acct_no+'</td>'
			s+='<td>'+row.fk_date+'</td>'
			s+='<td>'+row.cust_name.decode('gbk').encode('utf-8')+'</td>'
			s+='<td>'+str(row.amt)+'</td>'
			s+='</tr>'
			i+=1
		s+='<tr><td colspan="2" style="cursor:pointer" onClick="window.location.href=\'/records/?start='+str(start)+'&end='+str(end)+'&page='+str(int(page)-1)+'\'">上一页</td>'
		s+='<td colspan="2" style="cursor:pointer" onClick="window.location.href=\'/records/?start='+str(start)+'&end='+str(end)+'&page='+str(int(page)+1)+'\'">下一页</td></tr>'
		s+='</table>'

		response=HttpResponse(s)
		response.status_code=200
		return response	
	else:
		response=HttpResponse("Method not allowed")
		response.status_code=405
		return response

from datetime import datetime
import time
def record_modify_page(request,format,id):
	bb={}
	conn=pyodbc.connect('DRIVER={SQL Server};SERVER=12.31.0.29;DATABASE=jcb;UID=sa;PWD=Ceb4321')
	cur=conn.cursor()
	rate=cur.execute('select rate from rate').fetchone()[0]
	cur.execute('select * from bb')
	rows=cur.fetchall()
	for row in rows:
		bb[row[3]]=(float(row[2]),row[1])	
	if request.method=='GET' and format=='txt':
		cur.execute('select * from kehu where id=\''+id+'\'')
		rows=cur.fetchall()
		if rows==[]:
			raise Http404('Page not found.')
		row1=rows[0]
		cur.execute('select * from cltj where id=\''+id+'\' order by index_no;')
		rows=cur.fetchall()
		zhsy=0.0
		
		with open('site_media/download/record.html','w') as f:
			f.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
			f.write('<style type="text/css">p{font-size:15px;}table{border-collapse:collapse;border:spacing:0;overflow:hidden;font-size:15px;}td{border:1px solid #000000;height:30px;}</style></head><body>')
			f.write('&nbsp;'*10+'南京分行贷款业务综合收益测算表<br /><br />\n')
			f.write('<p>报送单位:(盖章)'+'&nbsp'*15+'电话:'+'&nbsp;'*15+'传真:</p>\n')
			f.write('<table>')

			f.write('<tr><td width=100px>客户名称</td><td width=200px>'+row1.cust_name.decode('gbk').encode('utf-8')[:39]+'</td><td width=100px>币别</td><td width=200px>'+bb[str(row1.bb)][1]+'</td></tr>\n')
			f.write('<tr><td>放款金额</td><td>'+str(row1.amt)+'</td><td>贷款利率</td><td>'+str(row1.dk_rate)+'% '+row1.sffd.decode('gbk').encode('utf-8')+'</td></tr>\n')
			f.write('<tr><td>风险资产</td><td>'+str(row1.risk_assets)+'</td><td>FTP</td><td>'+str(row1.FTP)+'%</td></tr>\n')
			dksyl=(float(row1.dk_rate)*0.945-float(row1.FTP))/100.0
			f.write('<tr><td>客户经理</td><td>'+row1.employee.decode('gbk').encode('utf-8')[:39]+'</td><td>贷款收益率</td><td>'+str(dksyl)+'</td></tr>\n')
			f.write('<tr><td>银票风险资产</td><td>'+str(row1.ypfxzc)+'</td><td>银票手续费收入</td><td>'+str(row1.ypsxfsr)+'</td></tr>\n')


			zhsy=(float(row1.amt)*float(row1.fk_qx)*dksyl-float(row1.risk_assets)*float(row1.fk_qx)*0.08*0.15)*float(bb[str(row1.bb)][0])-float(row1.ypfxzc)*float(row1.ypts)*0.08*0.15+float(row1.ypsxfsr)*360

			i=1
			for row in rows:
				f.write('<tr><td colspan="4">承诺条件:</td></tr>\n')

				f.write('<tr><td>存款客户名称</td><td>'+row.ck_cust_name.decode('gbk').encode('utf-8')[:39]+'</td><td>币别</td><td>'+bb[str(row.bb)][1]+'</td></tr>\n')
				cksyl=(float(row.FTP)-float(row.ck_rate))/100.0
				f.write('<tr><td>存款日均</td><td>'+str(row.ck_avg_day)+' '+row.psl.decode('gbk').encode('utf-8')+'</td><td>存款收益率</td><td>'+str(cksyl)+'</td></tr>\n')
				f.write('<tr><td>中间业务收入</td><td>%.2f'%(float(row.zjywsr))+'</td><td>其他条件</td><td>'+row.other_cond.decode('gbk').encode('utf-8')[:39]+'</td></tr>\n')
				zhsy+=(float(row.ck_avg_day)*cksyl*360+float(row.zjywsr)*360)*float(bb[str(row.bb)][0])
				i+=1
			if rows==[]:
				f.write('<tr><td colspan="4">承诺条件</td></tr>\n')
				f.write('<tr><td>存款客户名称</td><td></td><td>币别</td><td></td></tr>\n')

				f.write('<tr><td>存款日均</td><td></td><td>存款收益率</td><td></td></tr>\n')
				f.write('<tr ><td>中间业务收入</td><td></td><td>其他条件</td><td></td></tr>\n')
				
				
			f.write('<tr><td colspan="4">测算结果:</td></tr>\n')
			zhsy/=360.0
			f.write('<tr><td>综合收益</td><td>%.2f'%float(zhsy)+'</td>')
			suggest=(float(row1.amt)*float(rate)*float(row1.fk_qx)/36000.0-float(row1.risk_assets)*8*15*0.8*float(row1.fk_qx)/360.0/10000.0)*float(bb[str(row1.bb)][0])

			if zhsy>suggest:
				f.write('<td>综合收益建议</td><td></td></tr>\n')
			else:
				f.write('<td>综合收益建议</td><td>%.2f'%float(suggest)+'</td></tr>\n')
			f.write('<tr><td colspan="4">&nbsp;&nbsp;分行计财部审批意见'+'<br />'*15+'&nbsp;'*25+'负责人:'+'&nbsp;'*25+'年&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;日</td></tr>\n')
			f.write('</table>')
		conn.close()
		return HttpResponse('/site_media/download/record.html')
	elif request.method=='GET' and format=='json':
		cur.execute('select * from kehu where id=\''+id+'\'')
		rows=cur.fetchall()
		if rows==[]:
			response=HttpResponse('{"inform":"该记录不存在"}',mimetype="application/json")
			response.status_code=200
			return response
		row1=rows[0]
		cur.execute('select * from cltj where id=\''+id+'\' order by index_no;')
		rows=cur.fetchall()
		returnDic={'cust_name':row1.cust_name.decode('gbk').encode('utf-8'),'acct_no':str(row1.acct_no),'amt':str(row1.amt),'bb':str(row1.bb),'fk_date':str(row1.fk_date),'fk_qx':str(row1.fk_qx),'dk_rate':str(row1.dk_rate),'dk_profit':str(row1.dk_profit),'ftp':str(row1.FTP),'risk_assets':str(row1.risk_assets),'org':str(row1.org),'employee':row1.employee.decode('gbk').encode('utf-8'),'id':str(row1.id),'sffd':row1.sffd.decode('gbk').encode('utf-8'),'ypje':str(row1.ypje),'ypts':str(row1.ypts),'ypfxzc':str(row1.ypfxzc),'ypsxfsr':str(row1.ypsxfsr)}
		#print returnDic['cust_name'],row1.cust_name
		for row in rows:
			returnDic['ck_cust_name'+str(row.index_no)]=row.ck_cust_name.decode('gbk').encode('utf-8')
			returnDic['ck_acct_no'+str(row.index_no)]=str(row.ck_acct_no)
			returnDic['ck_avg_day'+str(row.index_no)]=str(row.ck_avg_day)
			returnDic['bb'+str(row.index_no)]=str(row.bb)
			returnDic['ck_qx'+str(row.index_no)]=str(row.ck_qx)
			returnDic['ck_rate'+str(row.index_no)]=str(row.ck_rate)
			returnDic['ftp'+str(row.index_no)]=str(row.FTP)
			returnDic['org'+str(row.index_no)]=str(row.org)
			returnDic['ck_profit'+str(row.index_no)]=str(row.ck_profit)
			returnDic['zjywsr'+str(row.index_no)]=str(row.zjywsr)
			returnDic['other_cond'+str(row.index_no)]=row.other_cond.decode('gbk').encode('utf-8')
			returnDic['psl'+str(row.index_no)]=row.psl.decode('gbk').encode('utf-8')

		response=HttpResponse(json.dumps(returnDic),mimetype="application/json")
		response.status_code=200
		return response
	elif request.method=='PUT':
		data=str(request.raw_post_data).replace(',}','}')
		data=json.loads(data)
		num=cur.execute('select count(*) from kehu where id=\''+id+'\'').fetchone()[0]
		if num!=1:
			response=HttpResponse('Conflict')
			response.status_code=409
			return response
		if data['cust_name'].replace(' ','')=='':
			response=HttpResponse('Conflict')
			response.status_code=409
			return response
		cur.execute('delete from cltj where id=\''+id+'\'')
		cur.execute('delete from kehu where id=\''+id+'\'')
		conn.commit()
		try:
			cur.execute('insert into kehu(cust_name,acct_no,amt,bb,fk_date,fk_qx,dk_rate,dk_profit,ftp,risk_assets,org,employee,middle_price,id,sffd,ypje,ypts,ypfxzc,ypsxfsr) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data['cust_name'],data['acct_no'],data['amt'],data['bb'],data['fk_date'],data['fk_qx'],data['dk_rate'],data['dk_profit'],data['ftp'],data['risk_assets'],data['org'],data['employee'],bb[data['bb']][0],id,data['sffd'],data['ypje'],data['ypts'],data['ypfxzc'],data['ypsxfsr'])
			conn.commit()
		except:
			response=HttpResponse('Conflict')
			response.status_code=409
			return response
		
		for i in range(1,21):
			if not data.has_key('ck_cust_name'+str(i)):
				break
			cur.execute('insert into cltj(acct_no,ck_cust_name,ck_acct_no,ck_avg_day,bb,ck_qx,ck_rate,ftp,ck_profit,org,zjywsr,other_cond,middle_price,index_no,id,psl) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data['acct_no'],data['ck_cust_name'+str(i)],data['ck_acct_no'+str(i)],data['ck_avg_day'+str(i)],data['bb'+str(i)],data['ck_qx'+str(i)],data['ck_rate'+str(i)],data['ftp'+str(i)],data['ck_profit'+str(i)],data['org'+str(i)],data['zjywsr'+str(i)],data['other_cond'+str(i)],bb[data['bb'+str(i)]][0],i,id,data['psl'+str(i)])
			conn.commit()
		conn.close()
		response=HttpResponse('Created')
		response.status_code=201
		return response
	elif request.method=='DELETE':
		try:
			cur.execute('delete from cltj where id=\''+id+'\'')
			cur.execute('delete from kehu where id=\''+id+'\'')
			conn.commit()
		except:	
			response=HttpResponse('Conflict')
			response.status_code=409
			return response
		response=HttpResponse('OK')
		response.status_code=200
		return response	
	else:
		response=HttpResponse("Method not allowed")
		response.status_code=405
		return response

def gz_acct_page(request,date,acct_no=''):
	conn=pyodbc.connect('DRIVER={SQL Server};SERVER=12.31.0.29;DATABASE=jcb;UID=sa;PWD=Ceb4321')
	cur=conn.cursor()
	sql='select kehu.cust_name,kehu.employee,fk_date,acct_no,amt*middle_price as \'amt\',b.balance from kehu,[12.31.0.118].[newage].[dbo].[r_sep_dg] b where CONVERT(varchar(8),DateAdd(day,fk_qx,fk_date),112)>=\''+date+'\' and kehu.acct_no=b.account_no and b.acc_type=\'loan\''

	if acct_no!='':
		sql+=' and kehu.acct_no=\''+acct_no+'\''

	sql+=' order by kehu.fk_date'
	cur.execute(sql)
	rows=cur.fetchall()
	
	returnList=[]
	for row in rows:
		try:
			item=cur.execute('select sum(ck_avg_day*middle_price),sum(zjywsr*middle_price) from cltj where acct_no=\''+row.acct_no+'\'').fetchone()
			ck_avg=item[0]
			zjywsr=item[1]
			item=cur.execute('select sum(ycr_avg_bal*middl_pric/100),sum(balance*middl_pric/100.0) from cltj a,[12.31.0.118].[newage].[dbo].[r_sep_dg] b where a.acct_no=\''+row.acct_no+'\' and a.ck_acct_no=b.account_no and b.acc_type=\'deposit\'')

			if item==[]:
				item=cur.execute('select sum(ycr_avg_bal*middl_pric/100),sum(balanc*middle_pric/100.0) from cltj c,[12.31.0.118].[newage].[dbo].[r_sep_sr] d where c.acct_no=\''+row.acct_no+'\' and c.ck_acct_no=d.account_no')
			if item!=[]:
				item=item.fetchone()
				dq_avg=item[0]
				balance=item[1]
		except:
			ck_avg=0.0
			dq_avg=0.0
			zjywsr=0.0
			balance=0.0
		if dq_avg is None:
			dq_avg=0.0
		if balance is None:
			balance=0.0
		if ck_avg is None:
			ck_avg=0.0
		if zjywsr is None:
			zjywsr=0.0
		returnList.append((row.cust_name,row.fk_date,str(row.acct_no)+'\t',str(row.amt),str(row.balance*-1),str(row.balance*-1-row.amt),str(ck_avg),str(balance),str(dq_avg),str(float(dq_avg)-float(ck_avg)),str(int(zjywsr))+'\t',row.employee))
		#[(row.acct_no,str(row.balance),str(row.balance-row.amt))]=(str(dq_avg),str(balance),str(balance-ck_avg),row.fk_date,str(zjywsr),row.cust_name,row.employee)
	if acct_no=='':
		rows=cur.execute('select cust_name,employee,fk_date,acct_no,amt*middle_price as \'amt\' from kehu where acct_no=\'\' and CONVERT(varchar(8),DateAdd(day,fk_qx,fk_date),112)>\''+date+'\' order by kehu.fk_date')
		if rows!=[]:
			for row in rows:
				returnList.append((row.cust_name,row.fk_date,str(row.acct_no)+'\t','','','','','','','',str(int(zjywsr))+'\t',row.employee))

	conn.close()
	string='客户名称,放款日期,放款账号,放款总额,当前贷款余额,变动,存款日均,当前存款余额,当前存款日均,变动,中间业务收入,客户经理\n'.decode('utf-8').encode('gbk')

	for it in returnList:
		string+=it[0]+','+it[1]+','+it[2]+','+it[3]+','+it[4]+','+it[5]+','+it[6]+','+it[7]+','+it[8]+','+it[9]+','+it[10]+','+it[11]+'\n'
	response=HttpResponse(string,content_type='text/csv')
	response['Content-Disposition']='attachment;filename=gz.csv'
	return response

@csrf_exempt
def rorac_page(request):
	if request.method!='POST':
		response=HttpResponse("Method not allowed")
		response.status_code=405
		return response
	rate=request.POST['rate']
	conn=pyodbc.connect('DRIVER={SQL Server};SERVER=12.31.0.29;DATABASE=jcb;UID=sa;PWD=Ceb4321')
	cur=conn.cursor()
	cur.execute('update rate set rate='+rate)
	conn.commit()
	conn.close()
	response=HttpResponse('<script type="text/javascript">alert("提交成功");window.location.href="/wh/";</script>')
	response.status_code=200
	return response


@csrf_exempt
def wh_bb_page(request):
	if request.method!='POST':
		response=HttpResponse("Method not allowed")
		response.status_code=405
		return response
	file=request.FILES.get('bb',None)
	if file==None:
		response=HttpResponse('Conflict')
		response.status_code=409
		return response
	
	text=file.read()
	text=text.split('\r\n')[1:]
	conn=pyodbc.connect('DRIVER={SQL Server};SERVER=12.31.0.29;DATABASE=jcb;UID=sa;PWD=Ceb4321')
	cur=conn.cursor()
	cur.execute('delete from bb;')
	conn.commit()


	for item in text:
		if item=='':
			break
		item=item.split(',')
		name=item[0].replace(' ','')
		if item=='':
			break
		bb=item[1].replace(' ','').replace('%','')
		rate=item[2].replace(' ','').replace('%','')
		code=item[3].replace(' ','').replace('%','')
		
		cur.execute('INSERT INTO bb VALUES(\'%s\',\'%s\',%.6f,\'%s\');'%(name,bb,float(rate),code))

	conn.commit()
	cur.execute('update kehu set middle_price=(select max(rate) from bb where bb.code=kehu.bb) from kehu,bb')
	conn.commit()

	cur.execute('update cltj set middle_price=(select max(rate) from bb where bb.code=cltj.bb) from cltj,bb')
	conn.commit()
	conn.close()
	response=HttpResponse('<script type="text/javascript">alert("提交成功");window.location.href="/wh/";</script>')
	response.status_code=200
	return response