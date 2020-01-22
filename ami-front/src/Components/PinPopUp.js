import React, {Component} from 'react';
import styles from './Style/PinStyle.css'
import axios from 'axios';
import backend from '../globals'
export default class PinPopUp extends Component{
    constructor(props){
        super(props);
        this.handleSubmit=this.handleSubmit.bind(this);
        this.handleDateChange=this.handleDateChange.bind(this);
        this.handleTextChange=this.handleTextChange.bind(this);
        this.handleDelete=this.handleDelete.bind(this);
        this.state = {
            visible: true
        }
    }
    getClass(){
        if(this.state.visible & !this.props.parent.hidden){
            return 'popup-div'
        }
        else{
            return 'hidden'
        }
    }
    getFormClass(){
        if(this.state.visible & !this.props.parent.hidden){
            return 'visible-form'
        }
        else{
            return 'hidden-form'
        }
    }
    handleSubmit(event){
        event.preventDefault();
        axios.get(`${backend.value}/notes/req/update_add_note/?id=${this.props.parent.state.id}&user=${this.props.parent.state.user}&field=${this.props.parent.state.field}&date=${this.props.parent.state.date}&latitude=${this.props.parent.state.latitude}&longitude=${this.props.parent.state.longitude}&value=${this.props.parent.state.value}`)
        console.log('pin saved')
    }
    handleDateChange(event){
        this.props.parent.setState({date: event.target.value});
    }
    handleTextChange(event){
        this.props.parent.setState({value: event.target.value});
    }
    handleDelete(){
        axios.get(`${backend.value}/notes/req/del_id/?id=${this.props.parent.state.id}`)
        .then(this.props.grandparent.startPinTimer())
        .then(this.props.grandparent.setState({pinsLoaded:false}));
        
    }
    render(){
        return (
            <div className={this.getClass()}>
                <form onSubmit={this.handleSubmit} className={this.getFormClass()}>
                    <label>
                        Date:
                        <input type='datetime' name="date" value={this.props.parent.state.date} onChange={this.handleDateChange}/>
                    </label>
                    <label>
                        Note:
                        <textarea type='text' name="text" value={this.props.parent.state.value} onChange={this.handleTextChange}/>
                    </label>
                    <div className='button-container'> 
                        <input type='submit' name="save" value="Save" className='input-button'/>
                        <input type='button' name="delete" value="Delete" className='input-button' onClick={this.handleDelete}/>
                    </div>
                    
                </form>

            </div>
        )
    }
}