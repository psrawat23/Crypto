// var detail={
//     name:"ram",
//     "class":"6th",
//     roll:34
// }

// console.log(detail.name.__proto__)


// const greet= ()=> "Helolo world ";

// console.log(greet());

// const promise_ex=function(call_back){
//     return new Promise((resolve,reject)=>{

//    setTimeout(function() { reject(call_back)},5000);
        
//     });
        
// }

// function a(){
//     console.log("you are successfully logged in ")
// }


// promise_ex(a).then((func) => func()).catch((reason)=>reason());


window.onscroll = () => console.log('scroll');



const promise= () =>{
    const apiKey = 'dc6zaTOxFJmzC'
    let url = `https://api.giphy.com/v1/gifs/trending?api_key=${apiKey}`;
    fetch(url)
    .then((data)=> data.json())
    .then((request)=>{
        request.data
        .map(gif=>gif.images.fixed_height.url)
        .forEach(url => {
            let img=document.createElement('img');
            img.src=url;
            document.body.appendChild(img);
        })
    }).catch(error => document.body.appendChild=error);
}
promise();