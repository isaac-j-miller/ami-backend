import React, {Component} from 'react'
import styles from './Style/SpinnerStyle.css'

export default class Spinner extends Component{
    constructor(props){
        super(props);
        this.state={visible:true}
        this.destroy=this.destroy.bind(this);
    }
    destroy(){
        this.setState({visible:false});
    }
    render(){
        return (
            <div className={this.state.visible? 'visible-spinner':'hidden-spinner'}>
                <button className='close' onClick={this.destroy}/>
                <img className='spinner-img' src='https://skyprecison.s3.amazonaws.com/res/spinner.gif'/>
                <p className='spinner-caption'>{this.props.caption}</p>
            </div>
        )
    }
}