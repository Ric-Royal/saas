from typing import Dict, List, Any
from sqlalchemy import func, desc, and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.models import Bill, BillAction, BillVote
from app.core.config import settings

class AnalyticsService:
    def get_summary_stats(self, db: Session) -> Dict[str, Any]:
        """Get summary statistics of bills"""
        total_bills = db.query(func.count(Bill.id)).scalar()
        bills_by_status = (
            db.query(Bill.status, func.count(Bill.id))
            .group_by(Bill.status)
            .all()
        )
        bills_by_type = (
            db.query(Bill.bill_type, func.count(Bill.id))
            .group_by(Bill.bill_type)
            .all()
        )
        
        return {
            "total_bills": total_bills,
            "by_status": {status: count for status, count in bills_by_status},
            "by_type": {bill_type: count for bill_type, count in bills_by_type}
        }

    def get_bill_trends(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get bill trends over time"""
        bills_over_time = (
            db.query(
                func.date_trunc('day', Bill.introduced_date).label('date'),
                func.count(Bill.id)
            )
            .filter(and_(
                Bill.introduced_date >= start_date,
                Bill.introduced_date <= end_date
            ))
            .group_by('date')
            .order_by('date')
            .all()
        )

        actions_over_time = (
            db.query(
                func.date_trunc('day', BillAction.action_date).label('date'),
                func.count(BillAction.id)
            )
            .filter(and_(
                BillAction.action_date >= start_date,
                BillAction.action_date <= end_date
            ))
            .group_by('date')
            .order_by('date')
            .all()
        )

        return {
            "bills_introduced": {
                str(date): count for date, count in bills_over_time
            },
            "bill_actions": {
                str(date): count for date, count in actions_over_time
            }
        }

    def get_popular_topics(
        self,
        db: Session,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get most popular bill topics based on metadata"""
        bills = db.query(Bill).all()
        topic_counts = {}
        
        for bill in bills:
            if bill.metadata and "topics" in bill.metadata:
                for topic in bill.metadata["topics"]:
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        sorted_topics = sorted(
            topic_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [
            {"topic": topic, "count": count}
            for topic, count in sorted_topics
        ]

    def analyze_bill(
        self,
        db: Session,
        bill: Bill
    ) -> Dict[str, Any]:
        """Get detailed analysis of a specific bill"""
        total_actions = db.query(func.count(BillAction.id)).filter(
            BillAction.bill_id == bill.id
        ).scalar()

        votes = db.query(BillVote).filter(BillVote.bill_id == bill.id).all()
        vote_analysis = []
        for vote in votes:
            total_votes = vote.yea_votes + vote.nay_votes + vote.abstain_votes
            vote_analysis.append({
                "date": vote.vote_date,
                "type": vote.vote_type,
                "result": vote.vote_result,
                "total_votes": total_votes,
                "yea_percentage": (vote.yea_votes / total_votes * 100) if total_votes > 0 else 0,
                "nay_percentage": (vote.nay_votes / total_votes * 100) if total_votes > 0 else 0,
                "abstain_percentage": (vote.abstain_votes / total_votes * 100) if total_votes > 0 else 0
            })

        return {
            "bill_id": bill.id,
            "total_actions": total_actions,
            "days_since_introduction": (datetime.utcnow() - bill.introduced_date).days,
            "vote_analysis": vote_analysis,
            "current_status": bill.status,
            "last_action_date": bill.last_action_date
        }

    def get_sponsor_activity(
        self,
        db: Session,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get most active bill sponsors"""
        bills = db.query(Bill).all()
        sponsor_counts = {}
        
        for bill in bills:
            if bill.sponsors:
                for sponsor in bill.sponsors:
                    sponsor_id = sponsor.get("id")
                    if sponsor_id:
                        if sponsor_id not in sponsor_counts:
                            sponsor_counts[sponsor_id] = {
                                "name": sponsor.get("name", "Unknown"),
                                "total_bills": 0,
                                "bills_passed": 0
                            }
                        sponsor_counts[sponsor_id]["total_bills"] += 1
                        if bill.status == "passed":
                            sponsor_counts[sponsor_id]["bills_passed"] += 1
        
        sorted_sponsors = sorted(
            sponsor_counts.items(),
            key=lambda x: x[1]["total_bills"],
            reverse=True
        )[:limit]
        
        return [
            {
                "sponsor_id": sponsor_id,
                "name": data["name"],
                "total_bills": data["total_bills"],
                "bills_passed": data["bills_passed"],
                "success_rate": (data["bills_passed"] / data["total_bills"] * 100)
                    if data["total_bills"] > 0 else 0
            }
            for sponsor_id, data in sorted_sponsors
        ]

    def get_bill_success_rate(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get bill success rate statistics"""
        bills = db.query(Bill).filter(and_(
            Bill.introduced_date >= start_date,
            Bill.introduced_date <= end_date
        )).all()

        total_bills = len(bills)
        passed_bills = sum(1 for bill in bills if bill.status == "passed")
        failed_bills = sum(1 for bill in bills if bill.status == "failed")
        pending_bills = total_bills - passed_bills - failed_bills

        return {
            "total_bills": total_bills,
            "passed_bills": passed_bills,
            "failed_bills": failed_bills,
            "pending_bills": pending_bills,
            "success_rate": (passed_bills / total_bills * 100) if total_bills > 0 else 0
        }

    def get_vote_patterns(
        self,
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get voting patterns analysis"""
        votes = db.query(BillVote).filter(and_(
            BillVote.vote_date >= start_date,
            BillVote.vote_date <= end_date
        )).all()

        total_votes = len(votes)
        vote_types = {}
        vote_results = {}
        margin_analysis = {
            "close_votes": 0,  # margin less than 5%
            "decisive_votes": 0,  # margin more than 20%
            "unanimous_votes": 0  # 100% yea or nay
        }

        for vote in votes:
            # Analyze vote types
            vote_types[vote.vote_type] = vote_types.get(vote.vote_type, 0) + 1
            
            # Analyze vote results
            vote_results[vote.vote_result] = vote_results.get(vote.vote_result, 0) + 1
            
            # Analyze margins
            total = vote.yea_votes + vote.nay_votes
            if total > 0:
                margin = abs(vote.yea_votes - vote.nay_votes) / total * 100
                if margin < 5:
                    margin_analysis["close_votes"] += 1
                elif margin > 20:
                    margin_analysis["decisive_votes"] += 1
                if margin == 100:
                    margin_analysis["unanimous_votes"] += 1

        return {
            "total_votes": total_votes,
            "vote_types": vote_types,
            "vote_results": vote_results,
            "margin_analysis": margin_analysis
        }

analytics_service = AnalyticsService() 