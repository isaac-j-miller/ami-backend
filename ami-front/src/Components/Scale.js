import React, {Component} from 'react'
import styles from './Style/ScaleStyle.css'
export default class Scale extends Component{
    constructor(props){
        super(props);
        this.state = {
            url:null
        }
    }
    componentDidMount(){
        if(this.props.parent.mapRef.current!==null){
            this.setState({url:this.props.parent.mapRef.current.state.activeOverlay.scale});
        }
    }
    render(){
        if(this.state.url!==null){
            return <img src={this.state.url} alt='color scale' className='color-scale'/>
        }
        else{
            return <div/>
        }
        
        
    }
}