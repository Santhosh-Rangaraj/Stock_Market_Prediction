import { STOCK_FORECAST_FAILURE, STOCK_FORECAST_REQUEST, STOCK_FORECAST_SUCCESS } from "../constants/forecastConstants"


export const forecastReducer = (state = {}, action) => {
	switch (action.type) {
		case STOCK_FORECAST_REQUEST:
			return {loading: true}
		case STOCK_FORECAST_SUCCESS:
			return {loading: false, info: action.payload}
		case STOCK_FORECAST_FAILURE:
			return {loading: false, error: action.payload}
		default:
			return state
	}
}