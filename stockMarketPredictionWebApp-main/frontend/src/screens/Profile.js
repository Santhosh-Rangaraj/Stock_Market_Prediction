import React, {useEffect} from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { getUserProfile } from '../actions/userActions'

const Profile = () => {

    const dispatch = useDispatch()

    const userProfile = useSelector((state) => state.userProfile)
    const { loading, error, info } = userProfile


    useEffect(() => {
		dispatch(getUserProfile())
        console.log(info)
	},[])	

    return (
        <div>Profile {info}</div>
    )
}

export default Profile