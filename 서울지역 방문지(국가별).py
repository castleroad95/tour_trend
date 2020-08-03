import requests
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib
import folium


API_KEY='79624d466663617338395861687a78'
API_KEY_decode=requests.utils.unquote(API_KEY)

output_type='json'
service='octastatapi10710'
start_index=1
end_index=100
gigan=2016
guckga=''

req_url='http://openapi.seoul.go.kr:8088/{0}/{1}/{2}/{3}/{4}/{5}/{6}/'.format(API_KEY_decode, output_type, service, start_index,end_index,gigan,guckga)
    
req_parameter={'KEY':API_KEY_decode,'TYPE':output_type,
              'SERVICE': service, 'START_INDEX':start_index,
              'END_INDEX':end_index ,'GIGAN': gigan,'GUCKGABYEOL':guckga
              }

r=requests.get(req_url,params=req_parameter)
dict_data=r.json()
#딕셔네리 키값 찾아나가기
dict_data.keys()

#dataframe하면서 column과 index설정(index가 숫자가 아닌 column에 있는 값으로 설정함)
col_list=['GIGAN','GUKGABYEOL','SARYESU','MYEONGDONG','DONGDAEMUNSIJANG','NAMTTAEMUNSIJANG','GOGUNG','NAMSANNSEOULTAWO','INSADONG','BANGMULGWANGINYEOMGWAN','JAMSILLOTDEWOLDEU','SINCHONHONGDAEJUBYEON','GANGNAMYEOK']
df_dict_data=pd.DataFrame(dict_data['octastatapi10710']['row'],columns=col_list)


#column과 index 명칭 바꾸기
df_dict_data_kor=df_dict_data.rename(columns={'GIGAN':'기간','GUKGABYEOL':'국가','SARYESU':'표본','MYEONGDONG':'명동','DONGDAEMUNSIJANG':'동대문시장','NAMTTAEMUNSIJANG':'남대문시장','GOGUNG':'경복궁','NAMSANNSEOULTAWO':'남산타워','INSADONG':'인사동','BANGMULGWANGINYEOMGWAN':'국립박물관','JAMSILLOTDEWOLDEU':'롯데타워','SINCHONHONGDAEJUBYEON':'홍대','GANGNAMYEOK':'강남'})
#그다음 인덱스 설정하기
df_dict_data_kor=df_dict_data_kor.set_index('국가')

#csv파일로 dataframe 저장하기
file_name='C:/Users/castl/Desktop/2020_job_academy/project/foreign_visitor_seoul/seoultourist.csv'
df_dict_data_kor.to_csv(file_name,sep=',',encoding='cp949')


#-----------------------------------------전체 데이터 정리 완료-----------------------------------

#원하는 columns 과 index설정 하여 데이터 추려내기
select_col=['명동','동대문시장','남산타워','롯데타워','홍대','강남']
select_index=['미국','호주','캐나다','일본','중국','태국','영국','프랑스','독일']
df_top5=df_dict_data_kor.loc[select_index]
df_top5=df_top5.drop(columns=['표본','기간'])


#표에 한글 가능하게 하기
matplotlib.rcParams['font.family']='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus']=False

#2016년 관광객 관광지 선호도 조사 plot생성
#T사용하여 index와 columns 교체
df_top5T=df_top5.T
print(df_top5T)

df_top5T=df_top5T.astype(float)
plot_top5=df_top5T.plot()
#반만 나오던 xticks값 나오게한 신의 한줄
plt.xticks(range(len(df_top5T.index)), df_top5T.index)
plt.xticks(rotation=45)
plot_top5.set_xlabel('서울 명소')
plot_top5.set_ylabel('방문율(%)')
plot_top5.set_title('2016년 관광객 관광지 선호도')
plt.show()

#-------------------------------------대륙별 선호 서울 관광지-------------------------------------------------
AS=['일본','중국','홍콩','싱가포르','대만','태국','말레이시아','인도']
EU=['독일','영국','프랑스','러시아']
NA=['미국','캐나다']


#대륙별 서울 명소 평균 비율(아시아,유럽,북미)
df_AS=df_dict_data_kor.loc[AS]
#drop으로 필요없는 행 제거
df_AS=df_AS.drop(columns=['표본','기간'])
df_AST=df_AS.T
#mean(axis=1)으로 행별 합 값을 구함
#.astype(float)으로 값을 float값으로 만듬
AST_mean=df_AST.astype(float).mean(axis=1)

df_EU=df_dict_data_kor.loc[EU]
df_EU=df_EU.drop(columns=['표본','기간'])
df_EUT=df_EU.T
EUT_mean=df_EUT.astype(float).mean(axis=1)

df_NA=df_dict_data_kor.loc[NA]
df_NA=df_NA.drop(columns=['표본','기간'])
df_NAT=df_NA.T
NAT_mean=df_NAT.astype(float).mean(axis=1)

df_all=df_dict_data_kor.drop(columns=['표본','기간'])
df_allT=df_all.T
#서울명소 별로 새로운 열의 값과 column을 추가
df_allT['AS평균']=AST_mean
df_allT['EU평균']=EUT_mean
df_allT['NA평균']=NAT_mean

##대륙별 평균값만 갖고 있는 차트만 추출
df_allT_mean=df_allT[['AS평균','EU평균','NA평균']]
print(df_allT_mean)

#bar그래프 형식으로 만듬
df_allT_mean.plot.bar(rot=0)
plt.ylabel('방문율(%)')
plt.xlabel('서울 명소')
plt.legend=(['ASIA','EU','NA'])
plt.xticks(rotation=45)
plt.show()


#-------------------------------------------지도에 전체 관광객 선호 지역 표시----------------------------------------
#초기 데이터에서 필요없는 columns 표본,기간을 삭제
df_global=df_dict_data_kor.drop(columns=['표본','기간'])
print(df_global)
df_globalT=df_global.T
print(df_globalT)
global_mean=df_globalT.astype(float).mean(axis=1)

#세계평균을 구하고 index명칭이 없던 index를 서울명소로 지정
df_globalT['세계평균']=global_mean
df_global_mean=df_globalT[['세계평균']]
df_global_mean.index.name='서울명소'
#서울명소를 column 으로 보내기 위해 reset사용, 인덱스를 기본 형태 로 바꿈
df_global_mean_re=df_global_mean.reset_index()

print(df_global_mean_re)


#각 서울명소에 해당하는 위도 경도를 차트로 만듬 
'''
명동  lat 37.5599  long 126.9858  
동대문시장  lat 37.5705  long 127.0078
남대문시장  lat 37.5595  long 126.9777
경복궁  lat  37.5806  long 126.9769
남산타워  lat 37.3306  long  126.5930
인사동   lat 37.5714  long 126.9861
국립박물관  lat 37.5247  long 126.9801
롯데타워  lat 37.5131 long  126.1026
홍대   lat 37.5570  long  126.9241
강남역 lat 37.4981 long 127.0276
'''
make_chart={'lat':[37.5599,37.5705,37.5595,37.5806,37.5513,37.5714,37.5247,37.5131,37.5570,37.4981],
            'long':[126.9858,127.0078,126.9777,126.9769,126.9881,126.9861,126.9801,127.1026,126.9241,127.0276]}
df_make_chart=pd.DataFrame(make_chart,columns=('lat','long'))
print(df_make_chart)
#join을 사용하여 세계평균과 서울명소를 위도,경도와 합침(인덱스가 동일해서 가능)
final_chart=df_global_mean_re.join(df_make_chart)
print(final_chart)

#folium을 사용 하여 원하는 지역 위도 경도 표시
seoul_map=folium.Map(location=[37.5599,126.9858],zoom_start=11.5,tiles='Stamen Toner')

#for문을 사용하여 서울명소를 지도에 각각의 위도경도에 맞게, 크기는 세계평균방문율에 맞게 설정
for i in final_chart.index:
    
    folium.CircleMarker([final_chart['lat'][i],final_chart['long'][i]],radius=final_chart['세계평균'][i]*0.4,
                        
                        color='#3186cc',fill_color='#3186cc',popup=(final_chart['서울명소'][i])).add_to(seoul_map)
#html파일로 저장    
seoul_map.save('C:/Users/castl/Desktop/2020_job_academy/project/foreign_visitor_seoul/seoul_map.html')