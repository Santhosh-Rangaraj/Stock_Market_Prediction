import { USER_LOGIN_FAILURE, USER_LOGIN_REQUEST, USER_LOGIN_SUCCESS, USER_LOGOUT, USER_PROFILE_FAILURE, USER_PROFILE_SUCCESS, USER_SIGNUP_FAILURE, USER_SIGNUP_REQUEST, USER_SIGNUP_SUCCESS } from "../constants/userConstants"
import axios from 'axios'

const baseUrl = "http://localhost:5000"

export const login = (email, password) => async (dispatch, getState) => {

	try {
		dispatch({type: USER_LOGIN_REQUEST})
		let config = {
			headers: { "Content-Type": "application/json" }
		}
		const {data} = await axios.post(baseUrl+'/user/login',{ email, password }, config) 
		console.log(data)
		// config = {
		// 	headers: {
		// 		Authorization: `Bearer ${data.access_token}`
		// 	}
		// }
		// const res = await axios.get(baseUrl+"/user/info", config)
		// data["name"] = res.data
		localStorage.setItem("userInfo", JSON.stringify(data))
		dispatch({
			type: USER_LOGIN_SUCCESS,
			payload: data
		})
	} catch (err) {
		console.log(err)
		dispatch({
			type: USER_LOGIN_FAILURE,
			payload: err.response.data.message
		})
	}
}

export const signup = (username, email, password) => async(dispatch) => {

	try {
		dispatch({ type: USER_SIGNUP_REQUEST})
		const config = {
			headers: { "Content-Type": "application/json" }
		}
		const {data} = await axios.post(baseUrl+'/user/register', {username, email, password},config)
        console.log(data)
		dispatch({
			type: USER_SIGNUP_SUCCESS,
			payload: data
		})
	} catch (err) {
		dispatch({
			type: USER_SIGNUP_FAILURE,
			payload: err.response.data.message
		})
	}
}

export const getUserProfile = () => async(dispatch, getState) => {
    try {
        dispatch({ type: USER_PROFILE_SUCCESS })
        const { userLogin: {userInfo} } = getState()

        const config = {
			headers: { 
                "Authorization": `Bearer ${userInfo.access_token}`,
                "Content-Type": "application/json"
            }
		}
        const {data} = await axios.get(baseUrl+'/user/profile',config)
		console.log(data["profile"])
        dispatch({ type: USER_PROFILE_SUCCESS, payload: data["profile"] })
    } catch(err) {
        dispatch({ type: USER_PROFILE_FAILURE, payload: err })
    }
}

export const logout = () => (dispatch) => {
	localStorage.removeItem("userInfo")
	dispatch({ type: USER_LOGOUT })
}