#!/usr/bin/env python
# coding: utf-8

# In[17]:


from solcx import compile_source,install_solc
install_solc()
compiled_sol=compile_source(
'''
pragma solidity ^0.8.14;
contract drugcompany
{
    struct product
    {
        uint avail;
        uint threosold;
        uint rate;
    }
    mapping (uint => product)drugs;
    address producer;
    address drugmanager;
    address hospitalmanager;
    // uint public prodid=0;
    uint orderdid=0;
    struct order
    {
        uint hospid;
        uint time;
        uint drugid;
        uint quantity;
        uint amount;
    }
    mapping (uint => order)orders;
    uint [] hospitals;
    uint public income=0;
       struct patient
   {
       uint hospid;
   }
   struct patient_log
   {
       uint patientid;
       uint docid;
       uint timestamp;
       uint drugid;
       uint amount;
   }
   uint [] patientarr;
   uint [] doctors;
   mapping (uint => patient) patients;
   mapping (uint => patient_log) logs;
   uint logid=1;
    modifier onlydm(address d)
    {
        require(d==drugmanager);
        _;
    }
    modifier onlyhm(address d)
    {
        require(d==hospitalmanager);
        _;
    }
    function reg_producer(address w) public onlydm(msg.sender)
    {
        producer=w;
    }
    constructor(address hm)
    {
        drugmanager=msg.sender;
        hospitalmanager=hm;
    }
    struct producer_content
    {
        uint amount;
    }
    mapping (uint => producer_content) produced_drug;
    modifier onlyproducer(address j)
    {
        require(j==producer);
        _;
    }
    function add_produced_drug(uint pid,uint a) public onlyproducer(msg.sender)
    {
        produced_drug[pid].amount=a;
    }
    function reg_hos(uint y) public onlyhm(msg.sender)
    {
        hospitals.push(y);
    }
    function reg_patient(uint y,uint hi) public onlyhm(msg.sender)
    {
        patientarr.push(y);
        patients[y].hospid=hi;
    }
        function reg_doctor(uint y) public onlyhm(msg.sender)
    {
        doctors.push(y);
    }
    modifier validam(uint d,uint p)
    {
        require(produced_drug[p].amount==d);
        _;
    }
    function add_drug(uint p,uint a,uint t,uint r) public onlydm(msg.sender) validam(a,p)
    {
       drugs[p].avail=a;
        drugs[p].threosold=t;
        drugs[p].rate=r;
        // prodid+=1;
    }
    function update_avail(uint pi,uint k) public onlydm(msg.sender) validam(k,pi)
    {
        drugs[pi].avail+=k;
    }
    function valid_hos(uint j) private returns(bool)
    {
        uint flag=0;
        for(uint i=0;i<hospitals.length;i++)
        {
            if(hospitals[i]==j)
            {
                flag=1;
                return true;
            }
        }
        if (flag==0)
        {
            return false;
        }
    }
        function valid_pait(uint j) private returns(bool)
    {
        uint flag=0;
        for(uint i=0;i<patientarr.length;i++)
        {
            if(patientarr[i]==j)
            {
                flag=1;
                return true;
            }
        }
        if (flag==0)
        {
            return false;
        }
    }
        function valid_doctors(uint j) private returns(bool)
    {
        uint flag=0;
        for(uint i=0;i<doctors.length;i++)
        {
            if(doctors[i]==j)
            {
                flag=1;
                return true;
            }
        }
        if (flag==0)
        {
            return false;
        }
    }
    modifier validhos(uint tr)
    {
        require(valid_hos(tr)==true);
        _;
    }
      modifier validp(uint tr)
    {
        require(valid_pait(tr)==true);
        _;
    }
      modifier validd(uint tr)
    {
        require(valid_doctors(tr)==true);
        _;
    }
    modifier meetavail(uint hy,uint k)
    {
        require(hy<= drugs[k].avail);
        _;
    }
    modifier meetthros(uint k,uint hy)
    {
        require(hy< drugs[k].threosold);
        _;
    }
      function buy_drug (uint h,uint porid,uint req_amount,uint did,uint patid) public validhos(h) meetavail(req_amount,porid) meetthros(porid,req_amount) validp(patid) validd(did)
    {
        drugs[porid].avail-=req_amount;
        income+=(req_amount*drugs[porid].rate);
        orders[orderdid].hospid=h;
        orders[orderdid].time=block.timestamp;
        orders[orderdid].drugid=porid;
        orders[orderdid].quantity=req_amount;
        orders[orderdid].amount=req_amount*drugs[porid].rate;
        orderdid+=1;
       logs[logid].patientid=patid;
        logs[logid].docid=did;
        logs[logid].timestamp=block.timestamp;
        logs[logid].drugid=porid;
        logs[logid].amount=req_amount;
        logid+=1;
    }
    function drug_av(uint pid) view public returns(uint) 
    {
        return drugs[pid].avail;
    }
}
'''
    ,output_values=['bin','abi']
)


# In[18]:


from web3 import Web3
contract_id,contract_interface=compiled_sol.popitem()
b=contract_interface['bin']
a=contract_interface['abi']
w3=Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
drugcompany=w3.eth.contract(abi=a,bytecode=b)


# In[19]:


drugcompany


# In[22]:


non=w3.eth.getTransactionCount("0xb37b35FFA5f963619dc669C77eb69BdF5F4382bE")
addr="0x677227fE7eC41609c040Dd4fB2f005842F5325F5"
trans=drugcompany.constructor(addr).buildTransaction(
    {
         "gasPrice":w3.eth.gas_price,
    "from":"0xb37b35FFA5f963619dc669C77eb69BdF5F4382bE",
    "nonce":non
    })


# In[23]:


p="0x10437b37afb4bc973fb52bab5697135ce0d08aca8a3fe8ca3a323747b6db2777"
signed_tx=w3.eth.account.sign_transaction(trans,private_key=p)


# In[24]:


signed_tx


# In[25]:


tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)


# In[26]:


tx_recipt=w3.eth.wait_for_transaction_receipt(tx_hash)


# In[ ]:




