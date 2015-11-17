# -*- coding: utf-8 -*-
import requests
import xlrd
import xlwt

# constants
ak = 'bGsFj1kA8NacYNGk9fAA5i00'
service_url = 'http://api.map.baidu.com/direction/v1'

xls_name = 'Book-utf-8.xls'
sheet_name = 'Sheet2'
provice_name = ("北京","天津","河北","山西","内蒙古","辽宁","吉林","黑龙江","上海","江苏","浙江","安徽","新疆","青海","宁夏","甘肃","陕西","西藏","云南","贵州","四川","重庆","海南","广西","广东","湖南","湖北","河南","山东","江西","福建")


def chose_counter(mode):
	"""选择列循环迭代范围的counter"""
	count = range(len(provice_name)+1)
	if mode == 1:
		# thread 1
		counter = count[1:32]
		return counter
		
		
def	xls_read(xls_name,sheet_name):
	"""读取xls文件得到指定Sheet的table"""
	data = xlrd.open_workbook(xls_name)
	table = data.sheet_by_name(sheet_name)
	return table
	
	
def gen_req_dict(origin,destination):
	"""生成需要查询的城市在Direction API 请求的parameters
		Direction API是一套以http形式提供的公交、驾车、步行查询检索接口,
		返回xml或json格式的检索数据,可用于实现开发线路规划功能
	"""
	# init dict
	req_dict = {}
	# constants
	req_dict['mode'] = 'driving'
	req_dict['output'] = 'json'
	req_dict['ak'] = ak
	# setup
	req_dict['origin'] = origin
	req_dict['origin_region'] = origin
	req_dict['destination'] = destination
	req_dict['destination_region'] = destination
	return req_dict
	
	
def crawler(url,param_dict):
	"""带参数从 API get 到需要的信息"""
	result = requests.get(url,params=param_dict).json()
	if result['status'] == 0 and result['type'] == 2:
		distance = result['result']['routes'][0]['distance'] / 1000
		duration = result['result']['routes'][0]['duration'] / 3600
		return (distance,duration)
	else:
		return 'error between the if of crawler'
		
	
def xls_writer(sheet,plat_table):
	nVec = len(plat_table)
	for y in range(nVec):
		for x in range(nVec):
			sheet.write(y,x,plat_table[y][x])
			
def xls_saver(filename,dista_table,dur_table):
	"""将结果写入新建名称为每列第一个字符串的xls文件,
	sheet名称将分别为distance和duration，
	并在table内体现出对称矩阵形式利于matlab进行处理。
	"""
	xls_handler = xlwt.Workbook(encoding='utf-8')
	sheet1 = xls_handler.add_sheet('distance')
	sheet2 = xls_handler.add_sheet('duration')
	xls_writer(sheet1,dista_table)
	xls_writer(sheet2,dur_table)
	# save
	xls_handler.save('%s.xls'% (filename) )
	
	
def main():
	"""流程"""
	# cols counter mode
	mode = 1
	# 取得城市table //checked
	table = xls_read(xls_name,sheet_name)
	# 迭代省cols下面的city。要注意的是下面的counter除了mode = 1 时候，它都不是从1开始的
	for i in range(31):
		city_name = (provice_name[i]).decode("utf-8") # 需要unicode来保存文件名
		temp_list = table.col_values(i) # temp_list 包含 省名称或直辖市名称
		# 处理空白
		try:
			list_length = temp_list.index('')
		except:
			print 'over'
			list_length = len(temp_list)
		city_list = temp_list[1:list_length] # city_list 为除去第一行省名称或直辖市名称的城市list
		city_list_len = list_length - 1
		# 2维矩阵存储查询结果
		plat_list1 = [[0 for col in range(city_list_len)] for row in range(city_list_len)]
		plat_list2 = [[0 for col in range(city_list_len)] for row in range(city_list_len)]
		# 省col只有单个城市时，将处理下一列
		if len(city_list) <= 1:
			continue
		# 其他情况，查询col里两两城市之间的距离
		else:
			# 查询两两距离的具体实现，将结果填充到2维矩阵
			for j in range(city_list_len):
				n = j+1
				origin = city_list[j]
				print origin
				while n <= (city_list_len-1):
					destination = city_list[n]
					print destination
					# res = (distance,duration)
					res = crawler(service_url,gen_req_dict(origin,destination))
					print res
					plat_list1[j][n] = res[0]
					plat_list2[j][n] = res[1]
					n = n+1
			# 这里是for循环流程的继续		
			xls_saver(city_name,plat_list1,plat_list2)
	# 在mode = 1 的thread 查询 所有省会城市之间的距离
	# if mode == 1:
		
	
	
	
if __name__=="__main__":
	main()