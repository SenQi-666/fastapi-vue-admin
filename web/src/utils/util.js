import storage from 'store'

export function timeFix () {
  const time = new Date()
  const hour = time.getHours()
  return hour < 9 ? '早上好' : hour <= 11 ? '上午好' : hour <= 13 ? '中午好' : hour < 20 ? '下午好' : '晚上好'
}

export function getRangeDate (startDate, endDate) {
  let targetArr = [];
  let start = new Date(startDate);
  let end = new Date(endDate);
  let startDateInfo = {
    year: start.getFullYear(),
    month: start.getMonth() + 1,
    day: start.getDate() 
  };
  let endDateInfo = {
    year: end.getFullYear(),
    month: end.getMonth() + 1,
    day: end.getDate() 
  };
  if(startDateInfo.year === endDateInfo.year){  //同年
    if(startDateInfo.month !== endDateInfo.month){   //同年，不同月份
      //获取开始时间所在月的月底日期
      let startMax = new Date(startDateInfo.year, startDateInfo.month, 0).getDate();
      let endNum = startMax - startDateInfo.day + endDateInfo.day;
      for(let i = startDateInfo.day; i <= startDateInfo.day+endNum; i++){
        if(i > startMax){
          targetArr.push(`${endDateInfo.year}-${
            endDateInfo.month<10? 
            "0"+ endDateInfo.month: 
            endDateInfo.month
          }-${i-startMax < 10? "0" + (i-startMax): i-startMax}`);
        } else {
          targetArr.push(`${startDateInfo.year}-${
            startDateInfo.month<10? 
            "0"+ startDateInfo.month: 
            startDateInfo.month
          }-${i < 10? "0" + i: i}`);
        }
      }
    } else {  //同年同月
      for(let i = startDateInfo.day; i <= endDateInfo.day; i++){
        targetArr.push(`${startDateInfo.year}-${
          startDateInfo.month<10? 
          "0"+ startDateInfo.month: 
          startDateInfo.month
        }-${i<10? "0"+ i: i}`)
      }
    }
  } else {   //不同年   【既然不同年那肯定也不同月】
    let startMax = new Date(startDateInfo.year, startDateInfo.month, 0).getDate();
    let endNum = startMax - startDateInfo.day + endDateInfo.day;
    for(let i = startDateInfo.day; i <= startDateInfo.day+endNum; i++){
      if(i > startMax){
        targetArr.push(`${endDateInfo.year}-${
          endDateInfo.month<10? 
          "0"+ endDateInfo.month:
          endDateInfo.month
        }-${i-startMax < 10? "0" + (i-startMax): i-startMax}`);
      } else {
        targetArr.push(`${startDateInfo.year}-${
          startDateInfo.month<10? 
          "0"+ startDateInfo.month: 
          startDateInfo.month
        }-${i < 10? "0" + i: i}`);
      }
    }
  }
  
  return targetArr;
}

export function save_token (access_token, refresh_token, expires_in) {
  storage.set('Access-Token', access_token, new Date().getTime() + expires_in)
  storage.set('Refresh-Token', refresh_token)
}

export function listToTree (list) {
  let resultList = list.filter((item) => {
    let children = list.filter((child) => {
       return item.id === child.parent_id
    })
    if (children.length > 0) {
      item.children = children
    }
    return item.parent_id === null
  })
  return cloneDeep(resultList)
}

export function cloneDeep (obj) {
  return JSON.parse(JSON.stringify(obj));
}

export function isEmpty (obj) {
  if (obj === undefined || obj === null || obj === '') {
    return true;
  } else {
    return false;
  }
}