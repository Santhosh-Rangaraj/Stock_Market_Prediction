import { NEWS_ANALYSIS_FAILURE, NEWS_ANALYSIS_REQUEST, NEWS_ANALYSIS_SUCCESS, TWITTER_ANALYSIS_FAILURE, TWITTER_ANALYSIS_REQUEST, TWITTER_ANALYSIS_SUCCESS } from "../constants/AnalysisConstants"

export const twitterAnalysisReducer = (state = {}, action) => {
	switch (action.type) {
		case TWITTER_ANALYSIS_REQUEST:
			return {loading: true}
		case TWITTER_ANALYSIS_SUCCESS:
			return {loading: false, info: action.payload}
		case TWITTER_ANALYSIS_FAILURE:
			return {loading: false, error: action.payload}
		default:
			return state
	}
}

export const newsAnalysisReducer = (state = {}, action) => {
	switch (action.type) {
		case NEWS_ANALYSIS_REQUEST:
			return {loading: true}
		case NEWS_ANALYSIS_SUCCESS:
			return {loading: false, info: action.payload}
		case NEWS_ANALYSIS_FAILURE:
			return {loading: false, error: action.payload}
		default:
			return state
	}
}