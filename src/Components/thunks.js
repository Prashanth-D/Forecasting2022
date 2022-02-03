import {createForecast, loadForecastsSuccess, loadForecastsInProgress, loadForecastsFailure} from './actions';

export const loadForecasts = () => async (dispatch, getState) => {
    // dispatch(loadForecastsInProgress());
    //const response = await
};

export const addForecastRequest = text => async dispatch => {
    // try{
        //const body = JSON.stringify({text});
    //const response = await fetch(, {header:{}, method:'post, body,});
    //const forecast = await Response.json();
    //dispatch(createForecast(forecast));
   // }
   // catch (e){ dispatch(displayAlert(e));}
    
}

export const displayAlert = text => () => {
    alert(`You Clciked on : ${text}`);
};