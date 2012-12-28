import xlrd
import xlwt
import copy

from xlrd import open_workbook,cellnameabs
from xlwt import Style

wbOld = open_workbook("switch.xls",on_demand=True,formatting_info=True)
shOld = wbOld.sheet_by_index(0)

wbNew = xlwt.Workbook()
shNew = copy.deepcopy(wbOld.sheet_by_index(0))
wbNew._Workbook__worksheets.append(shNew)
shNew.set_name(shOld.name)

wbNew.save("switch-1st.xls")



	

