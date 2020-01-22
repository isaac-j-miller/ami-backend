import React, {Component} from 'react'
var ReactS3Uploader = require('react-s3-uploader');

export default class Uploader extends Component{
    constructor(props){
        super(props);
        this.state = {
            visible: false
        }
        this.s3Ref=React.createRef();
        this.onProgress=this.onProgress.bind(this);
        this.onFinish=this.onFinish.bind(this);
        this.onError=this.onError.bind(this);
    }
    getDivClassName(){
        if(this.state.visible){
            return 'uploader-visible'
        }
        else{
            return 'uploader-hidden'
        }
    }
    onProgress(event){

    }
    onFinish(event){

    }
    onError(event){

    }
    render(){
        return (
            <div className={this.getDivClassName()}>
                <ReactS3Uploader 
                    accept='application/zip'
                    onProgress={this.onProgress}
                    onFinish={this.onFinish}
                    onError={this.onError}
                    uploadRequestHeaders={{
                        'x-amz-acl': 'public-read'
                      }}
                    ref={this.s3Ref}/>
            </div>
        )
    }
}