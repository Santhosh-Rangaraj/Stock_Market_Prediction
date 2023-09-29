import { GET_DASHBOARD_FAILURE, GET_DASHBOARD_REQUEST, GET_DASHBOARD_SUCCESS } from "../constants/DashboardConstants"
import axios from "axios"


export const getDashboard = () => async(dispatch, getState) => {
	const baseUrl = "http://localhost:5000"
	try {
		dispatch({ type: GET_DASHBOARD_REQUEST })
		const { userLogin: {userInfo} } = getState()
		const config = {
			headers: { 
                "Authorization": `Bearer ${userInfo.access_token}`,
                "Content-Type": "application/json"
            }
		}
		console.log("hello")
		const {data} = await axios.get(baseUrl+'/user/dashboard', config)
		console.log("actions" + data)
		dispatch({ type: GET_DASHBOARD_SUCCESS, payload: data })
	} catch (err) {
		console.log(err)
		dispatch({ type: GET_DASHBOARD_FAILURE, payload:err })
	}
}