function search(){
    var input, filter, table, tr, td, i, txtValue
    input = document.getElementById("vendor_sale_search")
    filter = input.value.toUpperCase();
    table = document.getElementById("vendor_table")
    tr = table.getElementsByTagName("tr")
 
    for(i = 0; i < tr.length; i++){
        td = tr[i].getElementsByTagName("td");
        for(j=0; j < td.length; j++){
           var name = td[j].getElementsByClassName("card")[0].getElementsByTagName("div")[1].getElementsByTagName("div")[0].getElementsByTagName("h6")[0].getElementsByTagName("a")[0]
            if(name){
            txtValue = name.textContent || name.innerText
            if(txtValue.toUpperCase().indexOf(filter) > -1){
                td[j].style.display = ""
             console.log(txtValue.toUpperCase().indexOf(filter))
            }else{
                td[j].style.display = "none"
            }
        }
        }
    }
 
 }