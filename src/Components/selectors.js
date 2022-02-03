import { createSelector } from 'reselect';

export const getForecasts = state => state.forecasts.data;
export const getForecastsLoading = state => state.forecasts.isLoading;

export const getIncompleteForecasts = createSelector(
    getForecasts,
    getForecastsLoading,
    (forecasts, isLoading) => isLoading? [] : forecasts.filter(forecast => !forecast.isCompleted),
);

// getIncompleteForecasts(state)

export const getCompletedForecasts = createSelector(
    getForecasts,
    getForecastsLoading,
    (forecasts, isLoading) => isLoading? [] : forecasts.filter(forecast => !forecast.isCompleted),
);