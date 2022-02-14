// premetive data types

// string
var n = 'Himanshu';
console.log("my name is  "+n);
console.log("my data type  is  "+(typeof n));
// reference
let myarr = [1,2,3,false,'string']
console.log("my data type  is  "+(typeof myarr));

// object literals
let stMarks = {
himanshu : 40,
karan : 50
}

console.log("my data type  is  "+(typeof stMarks));

function MyName() {
    
}
console.log("my function data type  is  "+(typeof MyName));

let date = new Date();
 console.log(typeof date)

let myVar = String(35)
console.log("Type of 35 "+typeof myVar)

let arr = String([1,2,3,1,5])
console.log(arr.length,arr)

i = 8
console.log(i.toString())

stri = Number("12345")
console.log(stri,typeof stri)

stri1 = Number('zero')
console.log(stri1)
// let age = prompt("How old you are ?")
// alert(age)

// let isStu = confirm("You are student ?")
// alert(isStu)

// let yourName = prompt("What is your name ?",'')
// alert("Your Name is "+yourName)

// let age = prompt("How old you are ? ",'')

// let year = new Date()
// alert(year.getFullYear())
// alert(`You are around ${year.getFullYear()-age}`);

// if (age == 25) 
// {
//     alert("you are able for vote");
//     alert("you are so smart");

// }

// let j = 3;
// while (j)
// {
//     alert(j);
//     j--;
// }

// let j = 0 ;
// while(j) alert(j--);
// do 
// {
//     alert(j);
//     j++;
// }while(j < 3)

// for(k=0;k<3;k++)
// {
//     alert(typeof k)
// }

let sum = 0;

// while(true)
// {
//     let value = +prompt("enter number",'')
//     if(!value) break;

//     sum +=value
// }
// alert(sum)

// function showMsg(from,text="No text given")
// {
//     let msg = "Hello thi si smy first function  "
//     alert(from + ':' + text);
// }
// let ms = showMsg()
// showMsg("himanshu")
// ms("kiran")
// alert(showMsg)

// let a = prompt("Enter val 1");
// a=Number(a)
// // alert(typeof a)
// let b = prompt("Enter val 2");
// b=Number(b)
// let add = (a,b) => a+b
// alert(add(a,b))

// let dou = n => n*2

// alert(dou(4))
// alert(typeof dou)

// let ag = prompt("What is your age",18);

// let welcome = (ag<18)?
//     ()=>alert("You are not allowed"):
//     ()=> alert("Welcome");
// welcome()

// let uname = prompt("What is you name");
// let chekUname= confirm("Do you want to attend meeting ?")

// alert("User Name is "+uname);
// alert("He is come ?"+chekUname)

// let user ={
//     uname:"himanshu",
//     age : 25,
//     sayHello(){
//         alert(user.uname);
//         alert(this.age);

//     }

// };
// user.sayHello()


// *****async ,await,promise and callback example

const datas =[{uName:"Himanshu",age:25,proffesion:"Odoo Developer"},
              {uName:"Karan",age:24,proffesion:"Odoo Developer"}];

function getData(){

    let output="";
    setTimeout(()=>{datas.forEach((data,index)=>{
        output+=`<li>${data.uName}</li>`;

    })
    document.body.innerHTML=output;
    },500);
        }

function createData(newData){

    return new Promise((resolve,reject)=>{
        setTimeout(()=>{
            datas.push(newData);
            let error = false;
            if(!error){
                resolve();
            }else{
                reject("Something went wrong !!!")
            }
            },10000)
    })
   

}
    
createData({uName:"Harsh",age:25,proffesion:"Odoo Developer"}).then(getData);