import sys
import argparse
#from .atlisp import install_atlisp,pull,pkglist,search

# from .search import search
parser = argparse.ArgumentParser(
    prog="atlisp",usage="atlisp command <pkgname/keystring>",
    description='@lisp是一个运行于 AutoCAD、中望CAD、浩辰CAD及类似兼容的CAD系统中的应用管理器。')
parser.add_argument("command",help="执行 atlisp 命令")

help_str = """usage: atlisp.exe command <pkgname/keystring>
@lisp是一个运行于 AutoCAD、中望CAD、浩辰CAD及类似兼容的CAD系统中的应用管理器。

command       function:
  pull        安装@lisp包 到 CAD
  install     安装@lisp Core 到 CAD
  list        列已安装的@lisp包
  search      联网搜索 @lisp 包

options:
  -h, --help  show this help message and exit
"""
    
import win32com.client,os
import time
install_str = '(progn(vl-load-com)(setq s strcat h "http" o(vlax-create-object (s"win"h".win"h"request.5.1"))v vlax-invoke e eval r read)(v o(quote open) "get" (s h"://atlisp.""cn/@"):vlax-true)(v o(quote send))(v o(quote WaitforResponse) 1000)(e(r(vlax-get-property o(quote ResponseText))))) '

def waitforcad(acadapp):
    while (not acadapp.GetAcadState().IsQuiescent):
        print(".",end="")
        time.sleep(1)
        
        
def install_atlisp():
    acadapp =win32com.client.Dispatch("AutoCAD.application")
    # 等待CAD忙完
    waitforcad(acadapp)
    acadapp.ActiveDocument.SendCommand('(setq @::backend-mode t) ')
    acadapp.ActiveDocument.SendCommand(install_str)
    acadapp.ActiveDocument.SendCommand("(@::set-config '@::tips-currpage 2) ")
    acadapp.ActiveDocument.Close(False)
    acadapp.Quit()
    
def pull(pkgname):
    print("安装 `" + pkgname + "' 到CAD 中")
    acadapp =win32com.client.Dispatch("AutoCAD.application")
    # 等待CAD忙完
    print("正在初始化dwg,请稍等",end="")
    # 确定是否安装了@lisp core
    #acadapp.ActiveDocument.SendCommand(install_str)
    waitforcad(acadapp)
    time.sleep(3)
    acadapp.ActiveDocument.SendCommand('(@::load-module "pkgman")(@::package-install-sub "'+ pkgname +'") ')
    print("\n正在安装 "+ pkgname+",请稍等",end="")
    waitforcad(acadapp)
    print("\n......完成")
    confirm = input("是否保持当前CAD实例，你可在当前实例中继续操作。(Y/N): ")
    if confirm.lower() in ['yes','y']:
        acadapp.visible=True
    else:
        acadapp.ActiveDocument.Close(False)
        acadapp.Quit()

def pkglist():
    "显示本地应用包"
    atlisp_config_path = os.path.join(os.path.expanduser(''),".atlisp") if os.name == 'posix' else os.path.join(os.environ['USERPROFILE'], '.atlisp')
    with open(os.path.join(atlisp_config_path,"pkg-in-use.lst"),"r") as pkglistfile:
        content = pkglistfile.read()
        print(content)

def search(keystring):
    print("联网搜索可用的应用包，开发中...")
    
def main():
    # target_function(*args,**kwargs)
    if len(sys.argv)>1:
        if sys.argv[1] ==  "pull":
            if len(sys.argv)>2:
                pull(sys.argv[2])
            else:
                print("Usage: atlisp pull pkgname")
                print("请指定包名 pkgname")
                print("示例: atlisp pull at-pm")
        elif sys.argv[1]  ==  "install" or sys.argv[1]=="i":
            print("安装@lisp到CAD中")
            install_atlisp();
            print("......完成")
        elif sys.argv[1]  ==  "list" or sys.argv[1]=="l":
            print("已安装的应用包:")
            print("---------------")
            pkglist()
            print("===============")
        elif sys.argv[1]  ==  "search" or sys.argv[1]=="s":
            if len(sys.argv)>2:
                print("搜索  " + sys.argv[2])
                search(sys.argv[2])
            else:
                 print("Usage: atlisp search keystring")
                 print("请给出要搜索的关键字")
                 print("示例: atlisp search pdf")
        elif sys.argv[1]=="-h" or sys.argv[1]=="--help":
            print(help_str)
        else:
            print("未知命令 "+ sys.argv[1])
    else:
        #parser.print_help()
        print(help_str)
if __name__ == "__main__":
    main()

    
