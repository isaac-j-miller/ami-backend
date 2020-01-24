import React, {Component} from 'react'
import styles from './Style/UploaderStyle.css'
import backend from '../globals'
import axios from 'axios'
import Dropzone from 'react-dropzone'
import AWS from 'aws-sdk'

const bucketRegion='us-east-1'
const IdentityPoolId = 'us-east-1:e485f93b-d5e0-4c80-b9be-06b4634869fb'

export default class Uploader extends Component{
    constructor(props){
        super(props);
        this.state = {
            visible: false,
            selectedFile: null,
            field:'',
            date:'',
            fieldsArray:[],
            addingField:false,
        }
        this.s3Ref=React.createRef();
        //this.onProgress=this.onProgress.bind(this);
        //this.onFinish=this.onFinish.bind(this);
        this.onError=this.onError.bind(this);
        this.onSubmit=this.onSubmit.bind(this);
        this.onClose=this.onClose.bind(this);
        this.onDrop=this.onDrop.bind(this);
        this.onFieldChange=this.onFieldChange.bind(this);
        this.onDateChange=this.onDateChange.bind(this);
        this.addField=this.addField.bind(this);
        this.onAddFieldChange=this.onAddFieldChange.bind(this);
    }
    getDivClassName(){
        if(this.state.visible){
            return 'uploader-visible'
        }
        else{
            return 'uploader-hidden'
        }
    }
    componentDidMount(){
        this.getFields();
    }
    onFieldChange(event){
        this.setState({field:event.target.value});
    }
    onDateChange(event){
        this.setState({date:event.target.value});
    }
    getFields(){
        this.setState({fieldsArray: this.props.parent.sideBarRef.current.state.fieldsArray});
    }
    onSubmit(event){
        event.preventDefault();
        if (this.state.date==="" | this.state.field==="" | !this.state.selectedFile[0] | !this.state.selectedFile[0].name.endsWith('.zip')){
            return
        }
        AWS.config.update({
            region: bucketRegion,
            credentials: new AWS.CognitoIdentityCredentials({
              IdentityPoolId: IdentityPoolId
            })
          });
        let keyGen = function(){
            let ans = '';
            let arr= 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
            for (let i = 20; i >0; i--){
                ans+=arr[Math.floor(Math.random()*arr.length)];
            }
            return `raw/${ans}.zip`
        }
        let key=keyGen();
        console.log(key);
        var upload = new AWS.S3.ManagedUpload({
            params: {
                Bucket: 'skyprecison',
                Key: key,
                Body: this.state.selectedFile[0],
                ACL: "public-read"
            }
        });
        
        let promise = upload.promise();
        let user = this.props.parent.state.user;
        let field=this.state.field;
        let date=this.state.date;
        let bands = ['blue', 'green', 'red', 'nir', 'red_edge', 'lwir'];
        promise.then(
            function(data) {
                console.log(data);
                alert("Successfully uploaded folder.");
                axios.get(`${backend.value}/raw/req/process/?user=${user}&field=${field}&date=${date}&url=${encodeURIComponent(data.Location)}&bands=${bands}`)
                .then(
                    console.log('request sent')
                )
        },
        function(err) {
            console.warn(err)
            return alert("There was an error uploading your folder: ", err);
        }
        );
        
        let generatedURL=`https://skyprecison.s3.amazonaws.com/${key}`
        console.log(generatedURL);
    }
    /*
    onProgress(event){

    }
    onFinish(event){

    }
    */
    onError(event){

    }
    
    onClose(event){
        this.setState({visible:false})
    }
    onDrop(file){
        console.log('dropped')
        console.log(file)
        this.setState({
            selectedFile:file
        });
    }
    addField(){
        this.setState({addingField:!this.state.addingField})
    }
    getNormalFieldClass(){
        if(!this.state.addingField){
            return 'hiddenfield-visible'
        }
        else{
            return 'hiddenfield-hidden'
        }
    }
    getHiddenFieldClass(){
        if(this.state.addingField){
            return 'hiddenfield-visible'
        }
        else{
            return 'hiddenfield-hidden'
        }
    }
    onAddFieldChange(event){
        this.setState({field: event.target.value})
    }
    render(){
        return (
            <div className={this.getDivClassName()}>
                <div className='uploader-backdrop'>
                    <button className='close' onClick={this.onClose}></button>
                    <form onSubmit={this.onSubmit}>
                        <label>Upload New Image Set</label>
                        <div>
                            <label>
                                Field:
                                
                                <input type='text' onChange={this.onAddFieldChange} className={this.getHiddenFieldClass()}/>
                                <select onChange={this.onFieldChange}className={this.getNormalFieldClass()}>
                                    {this.state.fieldsArray.map(function(element){
                                        return(
                                        <option key={element.key} value={element.value}>{element.value}</option>
                                    )})}
                                </select>
                            </label>
                            <input type='button' value='Add Field' onClick={this.addField}/>
                        </div>
                        <label>
                            Date:
                            <input type='date' onChange={this.onDateChange}/>
                        </label>
                    <div className='dropzone-div'>
                        <Dropzone onDrop={this.onDrop} >
                            {({getRootProps, getInputProps}) => (
                                <div {...getRootProps()} >
                                <input {...getInputProps()} className='dropzone'/>
                                    Drop your *.zip file which contains unprocessed images from the flight here!
                                </div>
                            )}
                        </Dropzone>
                    </div>
                    <input type='submit' value='Upload'/>
                    </form>
                </div>
            </div>
        )
    }
}