import React, {Component} from 'react'
import {Modal} from "react-bootstrap";
import {getMentorList, getStudentList} from "../../../../functions/services/api/group_requests/mentorStudentList";
import {createGroup} from "../../../../functions/services/api/group_requests/createGroup";

export default class CreateGroups extends Component {

    state = {
        Mentors: [],
        Students: [],
        selectedMentor: null,
        studentLists: [],
        mentorSearchQuery: '',
        studentSearchQuery: '',
        mentorSearchType: 'without_group',
        studentSearchType: 'without_group',
        groupName: ''
    };

    groupName = React.createRef()

    componentDidMount() {
        this.fetchMentorsList()
        this.fetchStudentList()

    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props !== prevProps) {
            this.setState({
                selectedMentor: null,
                studentLists: [],
                groupName: ""
            })

            this.fetchMentorsList()
            this.fetchStudentList()
        }
    }

    fetchMentorsList = () => {
        getMentorList(this, this.state.mentorSearchQuery, this.state.mentorSearchType);
    };

    fetchStudentList = () => {
        getStudentList(this, this.state.studentSearchQuery, this.state.studentSearchType);
    };

    handleSelectedMentor = (value) => {
        this.setState({selectedMentor: value})
    };

    handleStudentList = (event, value) => {
        const verify = event.currentTarget.checked;
        let {studentLists} = this.state;
        if (verify) {
            studentLists.push(value);
            this.setState({studentLists})
        } else {
            studentLists = studentLists.filter((data) => (
                data !== value
            ))
            this.setState({studentLists})
        }
    }

    submitForm = () => {
        // selectedMentor, studentLists
        let data = {
            name: this.groupName.current.value,
            mentor: this.state.selectedMentor.id,
            students: this.state.studentLists.map(student => student.id)
        }
        createGroup(this, data);
    }

    mentorSearch = (event) => {
        let mentorQuery = event.target.value.toLowerCase();
        this.setState({mentorSearchQuery: mentorQuery}, () => {
            this.fetchMentorsList()
        });
    }
    studentSearch = (event) => {
        let studentQuery = event.target.value.toLowerCase();
        this.setState({studentSearchQuery: studentQuery}, () => {
            this.fetchStudentList()
        });
    }

    mentorSelect = (event) => {
        this.setState({mentorSearchType: event.target.value}, () => {
            this.fetchMentorsList()
        })
    }
    studentSelect = (event) => {
        console.log(event.target.value)
        this.setState({studentSearchType: event.target.value}, () => {
            this.fetchStudentList()
        })
    }

    handleGroupNameChange = (event) => {
        console.log(event.target.value);
        this.setState({
            groupName: event.target.value
        })
    }

    render() {
        const {show} = this.props;
        const {Students, Mentors, selectedMentor, studentLists, groupName} = this.state;
        return (
            <>
                <button onClick={() => {
                    this.props.createGroupModal(true)
                }}><img src="https://icons.iconarchive.com/icons/custom-icon-design/mono-general-1/512/add-icon.png"
                        className="h-6" alt="add" onClick={() => {
                }}/></button>
                <Modal
                    size="lg"
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                    show={show} onHide={() => {
                    this.props.createGroupModal(true)
                }} animation={false}>

                    <div className="p-8">
                        <p className="text-center text-3xl"> Create Group</p>

                        <span className="absolute cursor-pointer font-medium p-6 right-0 text-2xl top-0"
                              onClick={() => {
                                  this.props.createGroupModal(false)
                              }}> X </span>
                        <div>
                            <div className="w-full p-1">
                                Group Name: <input className={'p-1'} placeholder={'Enter Group Name'}
                                                   ref={this.groupName} onChange={this.handleGroupNameChange}
                                                   value={groupName}/>
                            </div>
                            <div className="flex justify-around">

                                <div>
                                    <p className="text-center text text-lg">Mentor</p>
                                    <select className="my-1 w-full" onChange={this.mentorSelect}>
                                        <option value={'without_group'}>Mentor with no group
                                        </option>
                                        {/*<option value={'all'}>View All*/}
                                        {/*</option>*/}
                                    </select>
                                    <input className={'p-1 w-full'} type="search" placeholder="search"
                                           onChange={this.mentorSearch}/>
                                    <ul className="overflow-auto" style={{maxHeight: "130px"}}>
                                        {
                                            Mentors.length ? Mentors.map((data, index) =>
                                                (
                                                    <li className="flex" key={index}>
                                                        <input type="radio" name="mentor" className="mx-1 my-auto"
                                                               onClick={() => {
                                                                   this.handleSelectedMentor(data)
                                                               }}/><label className="my-auto">{data.user.email}</label>
                                                    </li>
                                                )) : 'No Data Found'
                                        }
                                    </ul>
                                </div>

                                <div>
                                    <p className="text-center text-lg">Student</p>
                                    <select className="my-1 w-full" onChange={this.studentSelect}>
                                        <option value={'without_group'}>Student with no group
                                        </option>
                                        <option value={'all'}>View All
                                        </option>
                                    </select>
                                    <input className={'p-1 w-full'} type="search" placeholder="search"
                                           onChange={this.studentSearch}/>
                                    <ul className="overflow-auto" style={{maxHeight: "130px"}}>
                                        {
                                            Students.length ? Students.map((data, index) =>
                                                (
                                                    <li className="flex" key={index}>
                                                        <input type="checkbox" className="mx-1 my-auto"
                                                               onClick={(event) => {
                                                                   this.handleStudentList(event, data)
                                                               }}
                                                               checked={studentLists.map(stu => stu.user.email).indexOf(data.user.email) !== -1}
                                                        /><label className="my-auto">{data.user.email}</label>
                                                    </li>
                                                )) : 'No Data Found'
                                        }
                                    </ul>
                                </div>
                            </div>

                            <div className="w-full my-2 border">
                                <p className="text-center text-2xl text-gray-700">Selected Students</p>
                                <div className="bg-green-200 p-4 flex overflow-auto"
                                     style={{flexFlow: "wrap", maxHeight: "190px"}}>
                                    {
                                        studentLists && studentLists.map((data, index) => (
                                            <p className="bg-gray-200 p-2 rounded mx-1" key={index}
                                               style={{width: "fit-content"}}>{data.user.email}
                                                <span
                                                    className={'bg-grey-100 cursor-pointer font-medium hover:shadow-md ml-1 rounded-full text-black translate-x-2'}
                                                    onClick={(event) => {
                                                        this.handleStudentList(event, data)
                                                    }}>???</span>
                                            </p>
                                        ))
                                    }
                                </div>
                            </div>

                            <div className="w-full my-2">
                                <p className="text-center text-2xl text-gray-700">Selected Mentor</p>
                                <p className="px-2 text-center text-2xl">{selectedMentor && (selectedMentor.user.email)}</p>
                            </div>

                            <div className="flex justify-center ">
                                <button
                                    className={`py-2 px-4 w-1/2 rounded bg-green-400 hover:bg-green-700 hover:text-white`}
                                    onClick={() => this.submitForm()}
                                    disabled={(!(selectedMentor && (studentLists.length && groupName.trim().length > 0)))}
                                >Create Group
                                </button>
                            </div>
                        </div>
                    </div>
                </Modal>
            </>
        )
    }
}
