import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from 'redux-thunk';
import { composeWithDevTools } from "redux-devtools-extension";
import { userLoginReducer, userProfileReducer, userSignupReducer } from "./reducers/userReducers";
import { newsAnalysisReducer, twitterAnalysisReducer } from "./reducers/analysisReducer";
import { forecastReducer } from "./reducers/forecastReducer";
import { dashboardReducer } from "./reducers/dashboardReducers";


const reducer = combineReducers({
	userLogin: userLoginReducer,
	userSignup: userSignupReducer,
    userProfile: userProfileReducer,
	twitterAnalysis: twitterAnalysisReducer,
	newsAnalysis: newsAnalysisReducer,
	stockForecast: forecastReducer,
	dashBoard: dashboardReducer,
})

const userInfoFromLocalStorage = localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo')) : undefined

const initialState = {
	userLogin: { userInfo: userInfoFromLocalStorage }
}

const middleware = [thunk]

const store = createStore(
	reducer,
	initialState,
	composeWithDevTools(applyMiddleware(...middleware))
)

export default store