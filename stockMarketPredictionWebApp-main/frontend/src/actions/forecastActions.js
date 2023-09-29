import axios from "axios"
import { STOCK_FORECAST_FAILURE, STOCK_FORECAST_REQUEST, STOCK_FORECAST_SUCCESS } from "../constants/forecastConstants"

export const getStockForecast = (companyname) => async(dispatch, getState) => {

	const baseUrl = "http://localhost:5000"
	try {
		dispatch({ type: STOCK_FORECAST_REQUEST })
		const { userLogin: {userInfo} } = getState()
		const config = {
			headers: { 
                "Authorization": `Bearer ${userInfo.access_token}`,
                "Content-Type": "application/json"
            }
		}
		const {data} = await axios.get(baseUrl + `/forecast/${companyname}`, config)
		dispatch({ type: STOCK_FORECAST_SUCCESS, payload: data})
	} catch (err) {
		console.log(err)
		dispatch({ type: STOCK_FORECAST_FAILURE, payload: err })
	}
}