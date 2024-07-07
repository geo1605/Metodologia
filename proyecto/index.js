
const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const cors = require('cors')
const app = express();
const port = 5000;
app.use(bodyParser.json());
app.use(cors());

const db = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'',
    database:'control_escolar',
});

app.post('/profesor/registrar', (req, res)=>{
    const { id, nombre, correo, direccion } = req.body;
    
    const sql = "INSERT INTO profesores VALUES(?,?,?,?)";
    db.query(sql, [id, nombre, correo, direccion], (err, result)=>{
        if(err) {
            res.status(300).send(err);
        }else {
            res.status(200).send(result)
        }
    });
});

app.put('/profesor/modificar/:id', (req, res)=>{
    const identificador = req.params.id;
    const { nombre, correo, direccion } = req.body;
    
    const sql = "UPDATE profesores SET nombre=?, correo=?, direccion=? WHERE id=?";
    db.query(sql, [ nombre, correo, direccion, identificador], (err, result)=>{
        if(err) {
            res.status(300).send(err);
        }else {
            res.status(200).send(result)
        }
    });
});


app.delete("/profesor/eliminar/:id", (req, res)=>{
    const id = req.params.id;
    const sql = 'DELETE FROM profesores WHERE id =?';
    db.query(sql, [id], (err, result)=>{
        if(err) {
            res.status(300).send(err);
        }else {
            res.status(200).send(result)
        }
    });
});

app.get("/", (req, res)=>{
    const sql = 'SELECT * FROM profesores';
    db.query(sql, (err, result)=>{
        if(err) {
            res.status(300).send(err);
        }else {
            res.status(200).send(result)
        }
    });
});

app.get("/profesor/editar/:id", (req, res) => {
    const id = req.params.id;
    const sql = 'SELECT * FROM profesores WHERE id=?';
    db.query(sql, [id], (err, result) => {
        if (err) {
            res.status(300).send(err);
        } else {
            if (result.length > 0) {
                res.status(200).json(result[0]);  // Devolver solo el primer resultado como JSON
            } else {
                res.status(404).send("Profesor no encontrado");  // Manejar caso de profesor no encontrado
            }
        }
    });
});


app.get("/profesor/:nombre", (req, res)=>{
    const nombre = req.params.nombre;
    const sql = 'SELECT * FROM profesores WHERE nombre LIKE ?';
    db.query(sql, [nombre], (err, result)=>{
        if(err) {
            res.status(300).send(err);
        }else {
            res.status(200).send(result)
        }
    });
});

/*
app.get("/profesores", (req, res)=>{
    const respuesta = {
        "id":1,
        "nombre":"Dagoberto Fiscal",
        "correo":"dago@gmail.com",
        "direccion":"5 de Febrero"
    }
    res.status(200).send(respuesta);
});
*/

app.all("*", (req, res)=>{
    const respuesta ={
        "codigo":300,
        "mensaje":"La ruta no existe"
    }
    res.send(respuesta)
});

app.listen(port, ()=>{
    console.log("Escuchando en el puerto 5000");
});