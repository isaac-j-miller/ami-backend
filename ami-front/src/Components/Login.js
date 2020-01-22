import React, {Component} from 'react';
import axios from 'axios'
import styles from '../Components/Style/LoginStyle.css'
class Login extends Component{
    constructor(props){
        super(props);
        this.state = {username: '',
                      password: ''}
        this.handleUsernameChange = this.handleUsernameChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleNewUser = this.handleNewUser.bind(this);
    }
    
    handleUsernameChange(event) {
        this.setState({username: event.target.value});
    }
    handlePasswordChange(event) {
        this.setState({password: event.target.value});
    }
    handleNewUser(){
        axios.get(`http://localhost:8000/users/req/get_next_id/?`)
        .then(res=>{
            const id = res.data.id;
            axios.get(`http://localhost:8000/users/req/add_user/?id=${id}&user=${this.state.username}&password=${this.state.password}`)
        }).then(this.logIn({fields:[],origins:{}}));
    }
    logIn(info){
        this.props.parent.state.user=this.state.username;
        this.props.parent.sideBarRef.current.state.user=this.state.username;
        let fields=info.fields;
        this.props.parent.state.fields=fields;
        this.props.parent.sideBarRef.current.state.fields=fields;
        this.props.parent.sideBarRef.current.getFields();
        this.props.parent.sideBarRef.current.getDates();
        this.props.parent.setState({loggedIn:true});
        this.props.parent.setState({origins:info.origins});
        this.props.parent.sideBarRef.current.setNewViewPort();
    }
    handleSubmit(event) {
        if(typeof event !== 'undefined'){
            event.preventDefault();
        }
        axios.get(`http://localhost:8000/users/req/authenticate/?user=${this.state.username}&password=${this.state.password}`)
        .then(res =>{
            const info = res.data;
            console.log(info);
            if(info.correct){
                this.logIn(info);
            }
            else{
                alert('Login Unsuccessful');
            }
        })
        .catch(function(error){
            console.warn(error);
        });
        
        
    }


    render(){
        return (
        <div className='login-wrapper'>
            <form onSubmit={this.handleSubmit}>
                <h1>skyprecision</h1>
                <label>Username:
                    <input type="text" name = "username" value={this.state.username} onChange={this.handleUsernameChange}/>
                </label>
                <label>Password:
                    <input type="password" name = "password" value={this.state.password} onChange={this.handlePasswordChange}/>
                </label>
                <div>
                    <input type="submit" name = "Log In" value="Log In" className='input-button'/>
                    <input type="button" name = "Create New Account" value="Create New Account" onClick={this.handleNewUser} className='input-button'/>
                </div>
            </form>
        </div>
        )
    }
}
export default Login