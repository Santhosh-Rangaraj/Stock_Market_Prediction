import { NEWS_ANALYSIS_FAILURE, NEWS_ANALYSIS_REQUEST, NEWS_ANALYSIS_SUCCESS, TWITTER_ANALYSIS_FAILURE, TWITTER_ANALYSIS_REQUEST, TWITTER_ANALYSIS_SUCCESS } from "../constants/AnalysisConstants"
import axios from 'axios'

const baseUrl = "http://localhost:5000"

export const getTwitterAnalysis = (companyname) => async(dispatch, getState) => {
	try {
		dispatch({ type: TWITTER_ANALYSIS_REQUEST })
		const { userLogin: {userInfo} } = getState()
		const config = {
			headers: { 
                "Authorization": `Bearer ${userInfo.access_token}`,
                "Content-Type": "application/json"
            }
		}
		const {data} = await axios.get(baseUrl+`/tweets/${companyname}`, config)
		console.log("action" + data)
		dispatch({ type: TWITTER_ANALYSIS_SUCCESS, payload: data })
	} catch (err) {
		console.log(err)
		dispatch({ type: TWITTER_ANALYSIS_FAILURE, payload:err })
	}
}

export const getNewsAnalysis = (companyname) => async(dispatch, getState) => {
	try {
		dispatch({ type: NEWS_ANALYSIS_REQUEST })
		const { userLogin: {userInfo} } = getState()
		const config = {
			headers: { 
                "Authorization": `Bearer ${userInfo.access_token}`,
                "Content-Type": "application/json"
            }
		}
		const {data} = await axios.get(baseUrl+`/news/${companyname}`, config)
		console.log(data)
		dispatch({ type: NEWS_ANALYSIS_SUCCESS, payload: data })
	} catch (err) {
		console.log(err)
		dispatch({ type: NEWS_ANALYSIS_FAILURE, payload:err })
	}
}