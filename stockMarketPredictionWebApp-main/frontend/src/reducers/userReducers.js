import { USER_LOGIN_FAILURE, USER_LOGIN_REQUEST, USER_LOGIN_SUCCESS, USER_LOGOUT, USER_PROFILE_FAILURE, USER_PROFILE_REQUEST, USER_PROFILE_SUCCESS, USER_SIGNUP_FAILURE, USER_SIGNUP_REQUEST, USER_SIGNUP_SUCCESS } from "../constants/userConstants";

export const userLoginReducer = (state = {}, action) => {
	switch (action.type) {
		case USER_LOGIN_REQUEST:
			return {loading: true}
		case USER_LOGIN_SUCCESS:
			return {loading: false, userInfo: action.payload}
		case USER_LOGIN_FAILURE:
				return {loading: false, error: action.payload}
		case USER_LOGOUT:
				return {}
		default:
			return state
	}
}

export const userSignupReducer = (state = {}, action) => {
	switch (action.type) {
		case USER_SIGNUP_REQUEST:
			return {loading: true}
		case USER_SIGNUP_SUCCESS:
			return {loading: false, info: action.payload}
		case USER_SIGNUP_FAILURE:
			return {loading: false, error: action.payload}
		case USER_LOGOUT:
			return {}
		default:
			return state
	}
}

export const userProfileReducer = (state = {}, action) => {
    switch (action.type) {
        case USER_PROFILE_REQUEST:
            return {loading: true}
        case USER_PROFILE_SUCCESS:
            return {loading: false, info: action.payload}
        case USER_PROFILE_FAILURE:
            return {loading: false, error: action.payload}
        default:
            return state
    }
}