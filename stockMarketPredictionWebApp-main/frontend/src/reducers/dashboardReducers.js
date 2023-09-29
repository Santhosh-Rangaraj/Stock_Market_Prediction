import { GET_DASHBOARD_FAILURE, GET_DASHBOARD_REQUEST, GET_DASHBOARD_SUCCESS } from "../constants/DashboardConstants"

export const dashboardReducer = (state = {}, action) => {
	switch (action.type) {
		case GET_DASHBOARD_REQUEST:
			return {loading: true}
		case GET_DASHBOARD_SUCCESS:
			return {loading: false, info: action.payload}
		case GET_DASHBOARD_FAILURE:
			return {loading: false, error: action.payload}
		default:
			return state
	}
}