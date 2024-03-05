    const log = document.getElementById("log");
function logInfo(name) {
    return function (course) {
        p = document.createElement('p');
        p.innerText = 'User ' + name + ' wants to take cources on ' + course;
        log.appendChild(p);
    }
}

oleg = logInfo('Oleg');
oleg('swimming');
oleg('karate');
oleg('yoga');
    function Client(first, last, age, gender){
        this._name={
            first, last
        };
        this._age =age;
        this._gender = gender;
    }
    Client.prototype={
        get name(){
            console.log('Getting name'+this._name);
            return this._name;
        },
        set name(name){
            console.log('Setting name');
            this._name=name;
        },
        get age(){
            console.log('Getting age'+this._age);
            return this._age;
        },
        set age(age){
            console.log('Setting age');
            this._age=age;
        },
        get gender(){
            console.log('Getting gender '+this._gender);
            return this._gender;
        },
        set gender(gender){
            console.log('Setting gender');
            this._gender = gender;
        },
    }
    Client.prototype.greeting = function(){
        alert("Hello! I am an ordinary client with name " + this.name.first+", "+this.name.last+ " with age: "+this.age+" gender: "+this.gender);
    }
    client = new Client('Oleg','Ohlabystin' ,23, 'male');
    client.greeting();
    function EliteClient(first, last, age, gender, money, profession){
        Client.call(this, first, last, age, gender);
        this._money = money;
        this._profession= profession;
    }
    //console.log(Object.getOwnPropertyNames(EliteClient.prototype));
    EliteClient.prototype = Object.create(Client.prototype);
    EliteClient.prototype.constructor = EliteClient;
    console.log("1--->"+EliteClient.prototype.constructor);
    Object.defineProperty(EliteClient.prototype, 'money', {
        get: function() {
            console.log('Getting EliteClient money '+this._money);
            return this._money;
        },
        set: function(money) {
            console.log('Setting EliteClient money');
            this._money= money;
        }
    });
    Object.defineProperty(EliteClient.prototype, 'profession', {
        get: function() {
            console.log('Getting EliteClient profession '+this._profession);
            return this._profession;
        },
        set: function(profession) {
            console.log('Setting EliteClient position_in_society');
            this._profession = profession;
        }
    });
    EliteClient.prototype.greeting = function () {
        var prefix;
        if (
            this.gender === "male" ||
            this.gender === "Male" ||
            this.gender === "m" ||
            this.gender === "M"
        ) {
            prefix = "Mr.";
        } else if (
            this.gender === "female" ||
            this.gender === "Female" ||
            this.gender === "f" ||
            this.gender === "F"
        ) {
            prefix = "Mrs.";
        } else {
            prefix = "Mx.";
        }
        alert(
            "Hello. I am EliteClient. My name is " + prefix + " " +
            this.name.last +" "+ this.name.first+
            " My age is: " + this.age+
            " My money is: " + this.money+
            " My profession is " +
            this.profession + "."
        );
    };
    eliteClient = new EliteClient('Alexey', 'Navalniy', 50,'Male',2000,'Prisoner');
    eliteClient.greeting();