from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os
import base64
import datetime


SECRET = os.getenv("SECRET")

#
app = FastAPI()

class Msg(BaseModel):
    msg: str
    secret: str

@app.get("/")

async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/homepage")
async def demo_get():
    driver=createDriver()

    homepage = getGoogleHomepage(driver)
    driver.close()
    return homepage

@app.post("/backgroundDemo")
async def demo_post(inp: Msg, background_tasks: BackgroundTasks):
    
    background_tasks.add_task(doBackgroundTask, inp)
    return {"message": "Success, background task started"}
    
@app.get("/execute/{user_info}")
def autoCommute(user_info: str): 
    def wait_until(xpath_str):
        WebDriverWait(driver,30).until(
        EC.presence_of_element_located((By.XPATH,xpath_str)))

    decoded_bytes = base64.b64decode(user_info)
    decoded_str = decoded_bytes.decode('utf-8')
    given_userid, given_userpw = decoded_str.split(":")
    userid = given_userid
    userpw = given_userpw
    print({"message": f"User {userid} confirmed successfully"})

    driver=createDriver()
    url = 'http://grw.itsnuh.com/gw/uat/uia/egovLoginUsr.do'
    driver.get(url)


    # 사용자 아이디 입력
    wait_until('//*[@id="userId"]')
    id = driver.find_element(By.XPATH, '//*[@id="userId"]')
    id.send_keys(userid)
    #사용자 패스워드 입력
    wait_until('//*[@id="userPw"]')
    pw = driver.find_element(By.XPATH, '//*[@id="userPw"]')
    pw.send_keys(userpw)
    #로그인 버튼 클릭
    wait_until('//*[@id="asp_login_a_type"]/div[2]/div[2]/span[1]/form/fieldset/div[2]/a')
    driver.find_element(By.XPATH,'//*[@id="asp_login_a_type"]/div[2]/div[2]/span[1]/form/fieldset/div[2]/a').click()
    
    #현재 시간 저장
    current_time = datetime.datetime.now().time()
    status = "출퇴근 전"
    #9시 이전일 경우 출근 진행, 9시 이후일 경우 퇴근 진행
    if current_time < datetime.time(9,1,0):
        #출근 탭 클릭
        wait_until('//*[@id="container"]/ul/li[1]')
        driver.find_element(By.XPATH,'//*[@id="container"]/ul/li[1]').click()
        #출근 버튼 클릭
        wait_until('//*[@id="inBtn"]')
        driver.find_element(By.XPATH,'//*[@id="inBtn"]').click()
        #출근 확인 버튼 클릭
        wait_until('//*[@id="btnConfirm"]')
        driver.find_element(By.XPATH,'//*[@id="btnConfirm"]').click()
        driver.quit()
        status = "출근 완료"
        return {
            "status": status,
            "currenttime": current_time
            }
    else:
        #퇴근 탭 클릭
        wait_until('//*[@id="container"]/ul/li[2]')
        driver.find_element(By.XPATH,'//*[@id="container"]/ul/li[2]').click()
        #퇴근 버튼 클릭
        wait_until('//*[@id="outBtn"]')
        driver.find_element(By.XPATH,'//*[@id="outBtn"]').click()
        #퇴근 확인 버튼 클릭
        wait_until('//*[@id="btnConfirm"]')
        driver.find_element(By.XPATH,'//*[@id="btnConfirm"]').click()
        driver.quit()
        status = "퇴근 완료"
        return {
            "status": status,
            "currenttime": current_time
            }

