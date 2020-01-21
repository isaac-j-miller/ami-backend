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
    }
    
    handleUsernameChange(event) {
        this.setState({username: event.target.value});
    }
    handlePasswordChange(event) {
        this.setState({password: event.target.value});
    }
    
    handleSubmit(event) {
        
        event.preventDefault();
        axios.get(`http://localhost:8000/users/?user=${this.state.username}&password=${this.state.password}`)
        .then(res =>{
            const info = res.data;
            console.log(info);
            if(this.state.password===info[0].password){
                
                this.props.parent.state.user=this.state.username;
                this.props.parent.sideBarRef.current.state.user=this.state.username;
                let fields=info[0].fields.split(',');
                this.props.parent.state.fields=fields
                this.props.parent.sideBarRef.current.state.fields=fields
                this.props.parent.sideBarRef.current.getFields()
                this.props.parent.sideBarRef.current.getDates()
                this.props.parent.setState({loggedIn:true})
            }
            else{
                alert('Login Unsuccessful')
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
                <h1>Log In</h1>
                <label>Username:
                    <input type="text" name = "username" value={this.state.username} onChange={this.handleUsernameChange}/>
                </label>
                <label>Password:
                    <input type="password" name = "password" value={this.state.password} onChange={this.handlePasswordChange}/>
                </label>
                <input type="submit" name = "submit"/>
                
            </form>
        </div>
        )
    }
}
export default Login